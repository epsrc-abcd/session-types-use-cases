Stencil
=======

The **Stencil** pattern is a commonly used pattern to update an element
in a structured grid with input from neighbouring elements. The pattern
comes from the calculation:


    for (i=1; i<N-1; i++) {
      for (j=1; j<M-1; j++) {
        A[i][j] = A[i-1][j] + A[i][j-1] + A[i][j] + A[i+1][j] + A[i][j+1]
      }
    }

Where the memory locations are treated as participants and memory
movement are interpreted as communication between them, which also
represents how the stencil calculation is performed in a distributed
system.
