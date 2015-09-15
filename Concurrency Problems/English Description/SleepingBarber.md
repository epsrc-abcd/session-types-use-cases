The use case presents a classic synchorisation problem. 
There is a barbershop with a separate waiting room. A barber is waiting for customers to arrive; when there are no customers the barber sleeps. When a customer arrives, he wakes the barber (if the barber is sleeping) or sits in one of the waiting chairs in the waiting room (if the barber is busy with other customer). If all chairs are occupied, the customer leaves. Customers repeatedly visit the barber shop until they get a haircut. The key element of the solution is to make sure that whenever a customer or a barber checks the state of the waiting room, they always see a valid state. The problem is implemented using a **Selector** actor that decides which is the next customer, **Customer** actors, a **Barber** actor, and a **Room** actor.

Link: https://www.cs.utexas.edu/users/EWD/transcriptions/EWD01xx/EWD123.html

