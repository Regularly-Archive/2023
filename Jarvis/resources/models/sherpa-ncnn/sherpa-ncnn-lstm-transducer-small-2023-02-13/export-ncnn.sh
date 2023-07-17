
exp_dir=lstm_transducer_stateless3/exp

./lstm_transducer_stateless3/export-for-ncnn.py \
    --exp-dir $exp_dir \
    --lang-dir data/lang_char \
    --epoch 40 \
    --avg 15 \
    --use-averaged-model True \
    --num-encoder-layers 8 \
    --rnn-hidden-size 320 \
    --encoder-dim 144 \
    --dim-feedforward 576 \
    --joiner-dim 320 \
    --decoder-dim 320
