The example is taken from the erlang benchmark suit (bencherl)
The use case presents many-to-many message passing scenario. Several
actors are spawned, each of which sends a **ping** message to another
random actor. Then the recipient actor responds with a **pong** message. A **Sink** actor
is notified **done** message about the completion of all interactions. When the **Sink** collects all replies, it
terminates the other actors. In an actor implementation, the benchmark measures the effects on contention on
the recipient's actor mailbox. In session types the use case requires
a join primitive, expressed in Scribble as a continuation after the
parallel branches. However, we are able to express causality between sending of the ping-pong messages and receiving the terminating $done$ message.
Note that the round robin sending cannot be precisely expressed in
Scribble. We have simplified the use case, giving only the type for two
ping-pong actors actor. The protocol can be extended
for more ping-pong actors if the configuration is fixed in
advance.

Link: http://www.softlab.ntua.gr/~gtsiour/files/erlang01-aronis.pdf
