Ring
====

The Ring protocol describes a wraparound pipeline pattern, where the
final participant (i.e. `Worker[N]`) of the pipeline sends a message back
to the first participant (i.e. `Worker[1]`) of the pipeline.

Note that the pattern is repeated `N-1` times, because each participant is
expected to hold `1/N` of the complete data set, and after `N-1` iterations
of the pipeline, all participants would have received the `1/N` of data
from other participants.
