FFT64
=====

The FFT64 protocol represents a 64-participant Fast Fourier
Transformation pattern, where 6 stages of butterfly exchanges are
performed between participants.

The expression `i + 1<<r - (1<<(r+1) * (i/(1<<r)%2))` is for calculating
the destination index of butterfly exchanges from `i`, where the
expression `1<<(r+1) * (i/(1<<r)%2)` calculates the direction (+/-) and
`1<<r` calculates the offset.
