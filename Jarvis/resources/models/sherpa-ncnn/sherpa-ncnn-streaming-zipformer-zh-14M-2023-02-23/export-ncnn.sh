#!/usr/bin/env bash

# Here are the model hyper-parameters required for model exporting

exp_dir=pruned_transducer_stateless7_streaming/exp-14M

python ./pruned_transducer_stateless7_streaming/export-for-ncnn-zh.py \
    --lang-dir data/lang_char \
    --exp-dir $exp_dir \
    --use-averaged-model True \
    --iter 400000 \
    --avg 8 \
    --decode-chunk-len 32 \
    --num-encoder-layers "2,3,2,2,3" \
    --feedforward-dims "320,320,640,640,320" \
    --nhead "4,4,4,4,4" \
    --encoder-dims "160,160,160,160,160" \
    --attention-dims "96,96,96,96,96" \
    --encoder-unmasked-dims "128,128,128,128,128" \
    --decoder-dim 320 \
    --joiner-dim 320

pushd $exp_dir

pnnx encoder_jit_trace-pnnx.pt
pnnx decoder_jit_trace-pnnx.pt
pnnx joiner_jit_trace-pnnx.pt

popd

# modify encoder_jit_trace-pnnx.ncnn.param to support sherpa-ncnn
# The following is the diff
# --- encoder_jit_trace-pnnx.ncnn.param-before    2023-02-14 20:48:52.000000000 +0800
# +++ encoder_jit_trace-pnnx.ncnn.param   2023-02-14 20:50:15.000000000 +0800
# @@ -1,5 +1,6 @@
#  7767517
# -2028 2547
# +2029 2547
# +SherpaMetaData           sherpa_meta_data1        0 0 0=2 1=32 2=4 3=7 15=1 -23316=5,2,4,3,2,4 -23317=5,384,384,384,384,384 -23318=5,192,192,192,192,192 -23319=5,1,2,4,8,2 -23320=5,31,31,31,31,31
#  Input                    in0                      0 1 in0
#  Input                    in1                      0 1 in1
#  Split                    splitncnn_0              1 2 in1 2 3
#
#------
# Explanation:
#
# (1) 2028 is changed to 2029 as an extra layer SherpaMetaData is added
# (2) SherpaMetaData is the layer type
# (3) sherpa_meta_data1 is the name of this layer. Must be sherpa_meta_data1
# (4) 0 0 means this layer has no input or output
# (5) 1=32, attribute 1, 32 is the value of --decode-chunk-len
# (6) 2=4, attribute 2, 4 is the value of --num-left-chunks
# (7) 3=7, attribute 3, 7 is the pad length. The first subsampling layer is using (x_len - 7) // 2, so we use 7 here
# (8) 15=1, attribute 15, 1 is the model version. We require it to be >=1 for sherpa-ncnn v2.0
# (9) -23316=5,2,4,3,2,4, attribute 16, this is an array attribute. It is attribute 16 since -23300 - (-23316) = 16
#       the first element of the array is the length of the array, which is 5 in our case.
#       2,4,3,2,4 is the value of --num-encoder-layers
# (10) -23317=5,384,384,384,384,384, attribute 17. 384,384,384,384,384 is the value of --encoder-dims
# (11) -23318=5,192,192,192,192,192, attribute 18, 192,192,192,192,192 is the value of --attention-dims
# (12) -23319=5,1,2,4,8,2, attribute 19, 1,2,4,8,2 is the value of --zipformer-downsampling-factors
# (13) -23320=5,31,31,31,31,31, attribute 20, 31,31,31,31,31 is the value of --cnn-module-kernels