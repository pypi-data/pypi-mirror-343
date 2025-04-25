import torch
from torch import nn
import torch.distributed as dist
import warnings
from typing import Optional, Union, List
from transformers.generation.stopping_criteria import (
    StoppingCriteriaList,
    validate_stopping_criteria,
)
from transformers.generation.logits_process import LogitsProcessorList
from transformers.generation.streamers import BaseStreamer
import time
from transformers.generation.utils import (
    SampleEncoderDecoderOutput,
    SampleDecoderOnlyOutput,
)

SampleOutput = Union[SampleEncoderDecoderOutput, SampleDecoderOnlyOutput]


def _sample(
    self,
    input_ids: torch.LongTensor,
    logits_processor: Optional[LogitsProcessorList] = None,
    stopping_criteria: Optional[StoppingCriteriaList] = None,
    logits_warper: Optional[LogitsProcessorList] = None,
    max_length: Optional[int] = None,
    pad_token_id: Optional[int] = None,
    eos_token_id: Optional[Union[int, List[int]]] = None,
    output_attentions: Optional[bool] = None,
    output_hidden_states: Optional[bool] = None,
    output_scores: Optional[bool] = None,
    return_dict_in_generate: Optional[bool] = None,
    synced_gpus: bool = False,
    streamer: Optional["BaseStreamer"] = None,
    **model_kwargs,
) -> Union[SampleOutput, torch.LongTensor]:
    new_generation_config = model_kwargs.pop("generation_config", None)
    if new_generation_config is not None:
        return_dict_in_generate = new_generation_config.return_dict_in_generate
        if not new_generation_config.do_sample:
            pad_token_id = new_generation_config._pad_token_tensor
            eos_token_id = new_generation_config._eos_token_tensor
            return self._greedy_search(
                input_ids,
                logits_processor,
                stopping_criteria,
                max_length,
                pad_token_id,
                eos_token_id,
                output_attentions,
                output_hidden_states,
                output_scores,
                return_dict_in_generate,
                synced_gpus,
                streamer,
                **model_kwargs,
            )
    else:
        pad_token_id = (
            pad_token_id
            if pad_token_id is not None
            else self.generation_config.pad_token_id
        )
        eos_token_id = (
            eos_token_id
            if eos_token_id is not None
            else self.generation_config.eos_token_id
        )
    token_latency = (
        self.config.token_latency if hasattr(self.config, "token_latency") else False
    )

    latency_list = []
    # init values
    logits_processor = (
        logits_processor if logits_processor is not None else LogitsProcessorList()
    )
    stopping_criteria = (
        stopping_criteria if stopping_criteria is not None else StoppingCriteriaList()
    )
    if max_length is not None:
        warnings.warn(
            "`max_length` is deprecated in this function, use"
            " `stopping_criteria=StoppingCriteriaList(MaxLengthCriteria(max_length=max_length))` instead.",
            UserWarning,
        )
        stopping_criteria = validate_stopping_criteria(stopping_criteria, max_length)
    logits_warper = (
        logits_warper if logits_warper is not None else LogitsProcessorList()
    )
    if isinstance(eos_token_id, int):
        eos_token_id = [eos_token_id]
    eos_token_id_tensor = (
        torch.tensor(eos_token_id).to(input_ids.device)
        if eos_token_id is not None
        else None
    )
    output_scores = (
        output_scores
        if output_scores is not None
        else self.generation_config.output_scores
    )
    output_attentions = (
        output_attentions
        if output_attentions is not None
        else self.generation_config.output_attentions
    )
    output_hidden_states = (
        output_hidden_states
        if output_hidden_states is not None
        else self.generation_config.output_hidden_states
    )
    return_dict_in_generate = (
        return_dict_in_generate
        if return_dict_in_generate is not None
        else self.generation_config.return_dict_in_generate
    )

    # init attention / hidden states / scores tuples
    scores = () if (return_dict_in_generate and output_scores) else None
    decoder_attentions = () if (return_dict_in_generate and output_attentions) else None
    cross_attentions = () if (return_dict_in_generate and output_attentions) else None
    decoder_hidden_states = (
        () if (return_dict_in_generate and output_hidden_states) else None
    )

    # if model is an encoder-decoder, retrieve encoder attention weights and hidden states
    if return_dict_in_generate and self.config.is_encoder_decoder:
        encoder_attentions = (
            model_kwargs["encoder_outputs"].get("attentions")
            if output_attentions
            else None
        )
        encoder_hidden_states = (
            model_kwargs["encoder_outputs"].get("hidden_states")
            if output_hidden_states
            else None
        )

    # keep track of which sequences are already finished
    unfinished_sequences = torch.ones(
        input_ids.shape[0], dtype=torch.long, device=input_ids.device
    )

    this_peer_finished = False  # used by synced_gpus only
    # auto-regressive generation
    while True:
        tic = time.time()
        if synced_gpus:
            # Under synced_gpus the `forward` call must continue until all gpus complete their sequence.
            # The following logic allows an early break if all peers finished generating their sequence
            this_peer_finished_flag = torch.tensor(
                0.0 if this_peer_finished else 1.0
            ).to(input_ids.device)
            # send 0.0 if we finished, 1.0 otherwise
            dist.all_reduce(this_peer_finished_flag, op=dist.ReduceOp.SUM)
            # did all peers finish? the reduced sum will be 0.0 then
            if this_peer_finished_flag.item() == 0.0:
                break

        if "past_key_values" in model_kwargs and not isinstance(
            model_kwargs["past_key_values"], tuple
        ):
            model_kwargs["past_key_values"] = None
        # prepare model inputs
        model_inputs = self.prepare_inputs_for_generation(input_ids, **model_kwargs)

        # forward pass to get next token
        self.model_backbone = self.config.architectures[0]
        if self.model_backbone in [
            "GPTJForCausalLM",
            "LlamaForCausalLM",
            "MllamaForConditionalGeneration",
            "GPTNeoXForCausalLM",
            "OPTForCausalLM",
            "FalconForCausalLM",
            "RWForCausalLM",
            "BloomForCausalLM",
            "CodeGenForCausalLM",
            "BaichuanForCausalLM",
            "ChatGLMModel",
            "GPTBigCodeForCausalLM",
            "T5ForConditionalGeneration",
            "MistralForCausalLM",
            "MixtralForCausalLM",
            "MptForCausalLM",
            "StableLmForCausalLM",
            "QWenLMHeadModel",
            "GitForCausalLM",
            "LlavaLlamaForCausalLM",
            "YuanForCausalLM",
            "PhiForCausalLM",
            "Phi3ForCausalLM",
            "Phi4MMForCausalLM",
            "WhisperForConditionalGeneration",
            "Qwen2ForCausalLM",
            "Maira2ForConditionalGeneration",
            "JambaForCausalLM",
            "DeepseekV2ForCausalLM",
            "DeepseekV3ForCausalLM",
        ]:
            first_token = False
            if hasattr(self.config, "kv_cache_dtype"):
                kv_cache_dtype = self.config.kv_cache_dtype
            elif hasattr(self, "dtype"):
                kv_cache_dtype = self.dtype
            else:
                kv_cache_dtype = torch.float
            input_bs = input_ids.size()[0]
            if model_inputs["past_key_values"] is None:
                first_token = True
                if self.model_backbone == "T5ForConditionalGeneration":
                    first_token = False
                    beam_idx_tmp = torch.zeros(
                        (2048, int(input_bs)), dtype=torch.long
                    ).contiguous()
                    model_inputs["past_key_values"] = tuple(
                        [
                            (
                                torch.zeros(1, 0, 0, 1, dtype=torch.long).contiguous(),
                                torch.zeros([1, 1, 1, 1])
                                .contiguous()
                                .to(kv_cache_dtype),
                                torch.zeros([1, 1, 1, 1])
                                .contiguous()
                                .to(kv_cache_dtype),
                                beam_idx_tmp,
                                torch.zeros(1, 0, 0, 1, dtype=torch.long).contiguous(),
                                self.decoder.block[i]
                                .layer[1]
                                .EncDecAttention.k(
                                    model_inputs["encoder_outputs"]["last_hidden_state"]
                                )
                                .view(
                                    int(input_bs),
                                    -1,
                                    self.decoder.block[i]
                                    .layer[1]
                                    .EncDecAttention.n_heads,
                                    self.decoder.block[i]
                                    .layer[1]
                                    .EncDecAttention.key_value_proj_dim,
                                )
                                .transpose(0, 1),
                                self.decoder.block[i]
                                .layer[1]
                                .EncDecAttention.v(
                                    model_inputs["encoder_outputs"]["last_hidden_state"]
                                )
                                .view(
                                    int(input_bs),
                                    -1,
                                    self.decoder.block[i]
                                    .layer[1]
                                    .EncDecAttention.n_heads,
                                    self.decoder.block[i]
                                    .layer[1]
                                    .EncDecAttention.key_value_proj_dim,
                                )
                                .transpose(0, 1),
                                beam_idx_tmp,
                            )
                            for i in range(self.config.num_hidden_layers)
                        ]
                    )
                if self.model_backbone == "WhisperForConditionalGeneration":
                    first_token = False
                    beam_idx_tmp = torch.zeros(
                        (2048, int(input_bs)), dtype=torch.long
                    ).contiguous()
                    model_inputs["past_key_values"] = tuple(
                        [
                            (
                                torch.zeros(1, 0, 0, 1, dtype=torch.long).contiguous(),
                                torch.zeros([1, 1, 1, 1])
                                .contiguous()
                                .to(kv_cache_dtype),
                                torch.zeros([1, 1, 1, 1])
                                .contiguous()
                                .to(kv_cache_dtype),
                                beam_idx_tmp,
                                torch.zeros(1, 0, 0, 1, dtype=torch.long).contiguous(),
                                self.model.decoder.layers[i]
                                .encoder_attn.k_proj(
                                    model_inputs["encoder_outputs"]["last_hidden_state"]
                                )
                                .view(
                                    int(input_bs),
                                    -1,
                                    self.model.decoder.layers[i].encoder_attn.num_heads,
                                    self.model.decoder.layers[i].encoder_attn.head_dim,
                                )
                                .contiguous(),
                                self.model.decoder.layers[i]
                                .encoder_attn.v_proj(
                                    model_inputs["encoder_outputs"]["last_hidden_state"]
                                )
                                .view(
                                    int(input_bs),
                                    -1,
                                    self.model.decoder.layers[i].encoder_attn.num_heads,
                                    self.model.decoder.layers[i].encoder_attn.head_dim,
                                )
                                .contiguous(),
                                beam_idx_tmp,
                            )
                            for i in range(self.config.num_hidden_layers)
                        ]
                    )

            if first_token:
                if hasattr(self.config, "n_layer"):
                    num_hidden_layers = self.config.n_layer
                elif hasattr(self.config, "num_hidden_layers"):
                    num_hidden_layers = self.config.num_hidden_layers
                elif hasattr(self.config, "text_config") and hasattr(
                    self.config.text_config, "num_hidden_layers"
                ):
                    num_hidden_layers = self.config.text_config.num_hidden_layers
                elif hasattr(self.config, "num_layers"):
                    num_hidden_layers = self.config.num_layers
                elif hasattr(self.config, "n_layers"):
                    num_hidden_layers = self.config.n_layers
                beam_idx_tmp = torch.zeros(
                    (2048, int(input_bs)), dtype=torch.long
                ).contiguous()
                if self.model_backbone == "GitForCausalLM":
                    num_head = self.git.encoder.layer[
                        0
                    ].attention.self.num_attention_heads
                    head_dim = int(
                        self.git.encoder.layer[0].attention.self.hidden_size / num_head
                    )
                    model_inputs["past_key_values"] = tuple(
                        [
                            (
                                torch.zeros(1, 0, 0, 1, dtype=torch.long).contiguous(),
                                torch.zeros([input_bs, num_head, 1, head_dim])
                                .contiguous()
                                .to(kv_cache_dtype),
                                torch.zeros([input_bs, num_head, 1, head_dim])
                                .contiguous()
                                .to(kv_cache_dtype),
                                beam_idx_tmp,
                            )
                            for i in range(num_hidden_layers)
                        ]
                    )
                elif self.model_backbone == "MllamaForConditionalGeneration":
                    head_dim = self.config.text_config.hidden_size // (
                        self.config.text_config.num_hidden_layers
                        - len(self.config.text_config.cross_attention_layers)
                    )
                    model_inputs["past_key_values"] = tuple(
                        [
                            (
                                (
                                    torch.zeros(
                                        1, 0, 0, 1, dtype=torch.long
                                    ).contiguous(),
                                    torch.zeros([1, 1, 1, 1])
                                    .contiguous()
                                    .to(kv_cache_dtype),
                                    torch.zeros([1, 1, 1, 1])
                                    .contiguous()
                                    .to(kv_cache_dtype),
                                    beam_idx_tmp,
                                )
                                if i
                                not in self.config.text_config.cross_attention_layers
                                else (
                                    torch.zeros([1, 1, 1, head_dim]).contiguous(),
                                    torch.zeros([1, 1, 1, head_dim]).contiguous(),
                                )
                            )
                            for i in range(num_hidden_layers)
                        ]
                    )
                elif self.model_backbone == "JambaForCausalLM":
                    intermediate_size = (
                        self.config.mamba_expand * self.config.hidden_size
                    )
                    conv_kernel_size = self.config.mamba_d_conv
                    ssm_state_size = self.config.mamba_d_state
                    dtype = (
                        self.config.dtype
                        if hasattr(self.config, "dtype")
                        else self.dtype
                    )
                    model_inputs["past_key_values"] = tuple(
                        [
                            (
                                (
                                    torch.zeros(
                                        1, 0, 0, 1, dtype=torch.long
                                    ).contiguous(),
                                    torch.zeros([1, 1, 1, 1]).contiguous(),
                                    torch.zeros([1, 1, 1, 1]).contiguous(),
                                    beam_idx_tmp,
                                )
                                if i % self.config.attn_layer_period
                                == self.config.attn_layer_offset
                                else (
                                    torch.zeros(
                                        input_bs,
                                        intermediate_size,
                                        ssm_state_size,
                                        dtype=dtype,
                                    ).contiguous(),
                                    torch.zeros(
                                        input_bs,
                                        intermediate_size,
                                        conv_kernel_size,
                                        dtype=dtype,
                                    ).contiguous(),
                                    torch.tensor(False).contiguous(),
                                )
                            )
                            for i in range(self.config.num_hidden_layers)
                        ]
                    )
                elif self.model_backbone in [
                    "DeepseekV2ForCausalLM",
                    "DeepseekV3ForCausalLM",
                ]:
                    model_inputs["past_key_values"] = tuple(
                        [
                            (
                                torch.zeros(1, 0, 0, 1, dtype=torch.long).contiguous(),
                                torch.zeros([1, 1, 1, 1])
                                .contiguous()
                                .to(kv_cache_dtype),  # latent_cache
                                beam_idx_tmp,
                            )
                            for i in range(num_hidden_layers)
                        ]
                    )
                else:
                    model_inputs["past_key_values"] = tuple(
                        [
                            (
                                torch.zeros(1, 0, 0, 1, dtype=torch.long).contiguous(),
                                torch.zeros([1, 1, 1, 1])
                                .contiguous()
                                .to(kv_cache_dtype),
                                torch.zeros([1, 1, 1, 1])
                                .contiguous()
                                .to(kv_cache_dtype),
                                beam_idx_tmp,
                            )
                            for i in range(num_hidden_layers)
                        ]
                    )
            if self.model_backbone == "LlavaLlamaForCausalLM" and hasattr(
                self, "prepare_inputs_labels_for_multimodal"
            ):
                model_inputs = self.prepare_inputs_labels_for_multimodal(**model_inputs)
            if first_token and self.model_backbone == "YuanForCausalLM":
                model_inputs.pop("past_key_values", None)
            if (
                not first_token
                and self.model_backbone == "Maira2ForConditionalGeneration"
            ):
                model_inputs.pop("pixel_values", None)
            if self.model_backbone == "WhisperForConditionalGeneration":
                model_inputs["encoder_outputs"] = (
                    model_inputs["encoder_outputs"]["last_hidden_state"],
                )
                model_inputs.pop("decoder_position_ids", None)
                model_inputs.pop("decoder_attention_mask", None)
            if self.model_backbone == "Phi3ForCausalLM":
                model_inputs.pop("inputs_embeds", None)
                model_inputs.pop("num_logits_to_keep", None)
            model_inputs.pop("cache_position", None)
            if hasattr(self, "trace_graph"):
                model_inputs.pop("use_cache", None)
                model_inputs.pop("token_type_ids", None)
                if "return_last_logit" in model_inputs:
                    model_inputs["return_last_logit"] = torch.tensor(
                        model_inputs["return_last_logit"]
                    )
                if self.model_backbone == "T5ForConditionalGeneration":
                    model_inputs.pop("head_mask", None)
                    model_inputs.pop("decoder_head_mask", None)
                    model_inputs.pop("decoder_attention_mask", None)
                    model_inputs.pop("cross_attn_head_mask", None)
                    model_inputs["encoder_outputs"] = (
                        model_inputs["encoder_outputs"]["last_hidden_state"],
                    )
                if self.model_backbone == "JambaForCausalLM":
                    model_inputs["output_router_logits"] = torch.tensor(
                        model_inputs["output_router_logits"]
                    )
                    model_inputs["num_logits_to_keep"] = torch.tensor(
                        model_inputs["num_logits_to_keep"]
                    )
                if first_token and hasattr(self, "trace_graph_first"):
                    outputs = self.trace_graph_first(**model_inputs)
                else:
                    outputs = self.trace_graph(**model_inputs)
            else:
                outputs = self(
                    **model_inputs,
                    return_dict=True,
                    output_attentions=output_attentions,
                    output_hidden_states=output_hidden_states,
                )
        else:
            outputs = self(
                **model_inputs,
                return_dict=True,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
            )

        if synced_gpus and this_peer_finished:
            continue  # don't waste resources running the code we don't need
        if isinstance(outputs, dict):
            next_token_logits = outputs.logits[:, -1, :]
        else:
            next_token_logits = outputs[0][:, -1, :]

        # pre-process distribution
        next_token_scores = logits_processor(input_ids, next_token_logits)
        next_token_scores = logits_warper(input_ids, next_token_scores)

        # Store scores, attentions and hidden_states when required
        if return_dict_in_generate:
            if output_scores:
                scores += (next_token_scores,)
            if output_attentions:
                decoder_attentions += (
                    (outputs.decoder_attentions,)
                    if self.config.is_encoder_decoder
                    else (outputs.attentions,)
                )
                if self.config.is_encoder_decoder:
                    cross_attentions += (outputs.cross_attentions,)

            if output_hidden_states:
                decoder_hidden_states += (
                    (outputs.decoder_hidden_states,)
                    if self.config.is_encoder_decoder
                    else (outputs.hidden_states,)
                )

        # sample
        probs = nn.functional.softmax(next_token_scores, dim=-1)
        next_tokens = torch.multinomial(probs, num_samples=1).squeeze(1)

        # finished sentences should have their next token be a padding token
        if eos_token_id is not None:
            if pad_token_id is None:
                raise ValueError(
                    "If `eos_token_id` is defined, make sure that `pad_token_id` is defined."
                )
            next_tokens = next_tokens * unfinished_sequences + pad_token_id * (
                1 - unfinished_sequences
            )

        # update generated ids, model inputs, and length for next step
        input_ids = torch.cat([input_ids, next_tokens[:, None]], dim=-1)
        if streamer is not None:
            streamer.put(next_tokens.cpu())
        model_kwargs = self._update_model_kwargs_for_generation(
            outputs, model_kwargs, is_encoder_decoder=self.config.is_encoder_decoder
        )

        # if eos_token was found in one sentence, set sentence to finished
        if eos_token_id_tensor is not None:
            unfinished_sequences = unfinished_sequences.mul(
                next_tokens.tile(eos_token_id_tensor.shape[0], 1)
                .ne(eos_token_id_tensor.unsqueeze(1))
                .prod(dim=0)
            )

            # stop when each sentence is finished
            if unfinished_sequences.max() == 0:
                this_peer_finished = True
        latency_list.append(time.time() - tic)
        unfinished_sequences = unfinished_sequences & ~stopping_criteria(
            input_ids, scores
        )
        # stop if we exceed the maximum length
        this_peer_finished = unfinished_sequences.max() == 0

        if this_peer_finished and not synced_gpus:
            break

    if streamer is not None:
        streamer.end()

    if return_dict_in_generate:
        if self.config.is_encoder_decoder:
            output_result = SampleEncoderDecoderOutput(
                sequences=input_ids,
                scores=scores,
                encoder_attentions=encoder_attentions,
                encoder_hidden_states=encoder_hidden_states,
                decoder_attentions=decoder_attentions,
                cross_attentions=cross_attentions,
                decoder_hidden_states=decoder_hidden_states,
            )
        else:
            output_result = SampleDecoderOnlyOutput(
                sequences=input_ids,
                scores=scores,
                attentions=decoder_attentions,
                hidden_states=decoder_hidden_states,
            )
    else:
        output_result = input_ids

    if token_latency:
        return (output_result, latency_list)
    else:
        return output_result
