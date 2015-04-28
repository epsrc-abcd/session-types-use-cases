Farm
====

The **Master-Worker** protocol, commonly known as the *Farm* pattern,
describes a one-to-many distribution pattern. In Pabble this is
implemented as a loop which a *Master* participant sends message
(distribute work) to each *Worker* participant then receive a reply from
them.
