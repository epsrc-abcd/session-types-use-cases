# CPGV

The examples in this directory are based on the languages CP and GV and their extensions.  CP is
something like a process calculus, with significant syntactic restriction, and GV is something like
a functional language.  The session type systems in both are limited---in particular, there's little
notion of interesting base types, and there aren't ideas like interruptions.  Background reading can
be found at:

* http://homepages.inf.ed.ac.uk/wadler/topics/linear-logic.html#propositions-as-sessions-jfp

  Original description of the CP and GV languages; discussion of the connection to linear logic.

* http://homepages.inf.ed.ac.uk/slindley/papers/cpgv.pdf

  Extensions of GV to be equivalent in expressivity to CP; reformulation of some terms.

* http://homepages.inf.ed.ac.uk/slindley/papers/mugv-draft-april2014.pdf

  Extension of both systems to incorporate recursive session types.

All the examples should be executable using the tools from https://github.com/jgbm/cpgv, modulo bugs
and infelicities in said tools.

## Notes on specific examples

### peano.cp/peano.gv

These examples encode Peano numerals in CP and GV.  The flavor of the encodings is slightly
different: both use recursive sessions, but the GV encodings wrap them to appear as return types.

### natstreams.cp

This encodes streams of naturals in various ways, including the Peano encoding from the previous
example.  It also demonstrates CP's very, very limited support for first-order (i.e., non-session)
types.

### sum.gv

Basically the calculator example from the recursion paper, but without multiplication.

### toninho.cp

Encoding of the bit strings example from the last series of Toninho, Caires and Pfenning papers.

### examples.gv

GV encodings of the examples from Propositions as Sessions; basically just reiterates all the usual
bookstore nonsense.
