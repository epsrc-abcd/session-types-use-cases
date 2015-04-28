Scatter Gather
==============

The **Scatter Gather** protocol is a common distribution and collection
pattern otherwise known as *Map-Reduce*, the Pabble protocol makes use
of collective (i.e. multirole) patterns to distribute data from one
participant (i.e. `Worker[1]`) to all participants with `__All`
(includes `Worker[1]` in our definition for practical reasons).
`Worker[1]` then performs the reverse pattern which collects data from
`__All`.
