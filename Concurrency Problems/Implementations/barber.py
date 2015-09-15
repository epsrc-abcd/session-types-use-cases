from cell.actors import Actor
from cell.roles import role, protocol, protocol_system_start, ProtocolMailbox
from cell.configuration import get_group_id, prot_config
import time
import random

c1, SleepingBarber, B, S, C, R, n = "c", "SleepingBarber", "B", "S", "C", "R", 'n'

@protocol(c1, SleepingBarber, B, [S, R, C], {C:n})
class Barber(Actor):
    class state(Actor.state):
        @role(c1)
        def join(self, c1, cid):
            self.actor.join(cid = cid)
            return True

        @role(c1)
        def enter(self, c1, cust_id):
            c1.C[cust_id].call.start()
            print 'The barber is sleeping!'
            time.sleep(random.randint(1, BarberConfig.random_max))
            c1.C[cust_id].call.done()
            c1.R.call.next()

        @role(c1, R)
        def wait(self, c1):
           print 'No customers. Going to sleep now.'


        @role(c1, R)
        def exit(self, c1):
            print 'Done for the day. Time to go for a beer!'

@protocol(c1, SleepingBarber, S, [R, B, C], {C:n})
class Selector(Actor):
    class state(Actor.state):
        @role(c1)
        def join(self, c1, cid):
            self.actor.join(cid = cid)
            self.numHairCutsSoFar=0
            print 'I am in Selector join.'
            return True

        @role(c1)
        def start(self, c1):
            for i in range(0, BarberConfig.haircuts):
                num = random.randint(0, BarberConfig.customers-1)
                time.sleep(random.randint(1, BarberConfig.random_max))
                c1.R.call.enter(cust_id = num)

        @role(c1, C)
        def done(self, c1):
            self.numHairCutsSoFar+=1
            if (self.numHairCutsSoFar == BarberConfig.haircuts):
                c1.R.call.exit()

        @role(c1, C)
        def returned(self, c1):
            num = random.randint(1, BarberConfig.customers)
            #c1.S[num].call.enter()
            c1.R.call.enter(num)

@protocol(c1, SleepingBarber, C, [R, B, S], {C:n}, True)
class Customer(Actor):
    class state(Actor.state):
        @role(c1)
        def join(self, c1, cid):
            self.actor.join(cid = cid)
            return True

        @role(c1, B)
        def start(self, c1):
            print 'I am now being served!'

        @role(c1, R)
        def full(self, c1):
            c1.S.call.returned()

        @role(c1, R)
        def wait(self, c1):
            print 'I will wait!'

        @role(c1, R)
        def done(self, c1):
            c1.S.call.done()
            print 'I have a new haircut!'

@protocol(c1, SleepingBarber, R, [B, S, C], {C:n})
class Room(Actor):
    class state(Actor.state):
        @role(c1)
        def join(self, c1, cid):
            self.actor.join(cid = cid)
            self.waiting_customers = []
            self.barber_asleep = True
            return True

        @role(c1, S)
        def enter(self, c1, num):
            if (len(self.waiting_customers) == BarberConfig.room_capacity):
                c1.C[num].call.full()
            else:
                self.waiting_customers.append(num)

                if self.barber_asleep:
                    self.barber_asleep = False
                    self.next()
                else:
                    c1.C[num].call.wait()
        @role(c1, B)
        def next(self, c1):
            if len(self.waiting_customers) >0:
                cust = self.waiting_customers.pop()
                c1.B.call.enter(cust)
            else:
                c1.B.call.wait()
                self.barber_asleep = True

        @role(c1, S)
        def exit(self, c1):
            c1.B.call.exit()
            print 'We are done'

class BarberConfig:
    room_capacity = 5
    random_max = 5
    haircuts = 3
    customers = prot_config[SleepingBarber][n]


def start_protocol():
    # On ActorSystem config
    protocol_system_start(SleepingBarber)
    # Start the protocol
    prot = ProtocolMailbox.create(SleepingBarber, [S])
    # Initiate the first action
    prot[S].call.start()

