from cell.actors import Actor
from cell.roles import role, protocol, protocol_system_start, ProtocolMailbox
from cell.configuration import get_group_id, prot_config
import random, time

c, CigaretteSmoker, A, S, n = "c", "CigaretteSmoker", "A", "S", 'n'

@protocol(c, CigaretteSmoker, A, [S], {S:n})
class Arbitrer(Actor):
    class state(Actor.state):
        @role(c)
        def join(self, c, cid):
            self.actor.join(cid=cid)
            self.roundSoFar = SmokersConfig.numRounds
            # sends a message to a random smokers
            return True

        @role(c)
        def start(self, c):
            self.notify_random_smoker(c)

        @role(c, S)
        def started_smoking(self, c):
            self.roundSoFar-=1
            if self.roundSoFar <=0:
                for i in range(0, SmokersConfig.numSmokers -1):
                    c.S[i].call.exit()
            else:
                self.notify_random_smoker(c)

        def notify_random_smoker(self, c):
            random_smoker = random.randint(0, SmokersConfig.numSmokers -1)
            busyWaitPeriod = random.randint(0, 100)
            c.S[random_smoker].call.start_smoking(wait = busyWaitPeriod)

@protocol(c, CigaretteSmoker, S, [A], {S:n})
class Smoker(Actor):
    class state(Actor.state):
        @role(c)
        def join(self, c, cid):
            self.actor.join(cid=cid)
            return True

        @role(c, A)
        def start_smoking(self, c, wait):
            c.A.call.started_smoking()
            time.sleep(wait)

        @role(c, A)
        def exit(self, c):
            print 'I am done.'

class SmokersConfig:
    numRounds = 3
    numSmokers = prot_config[CigaretteSmoker][n]

def start_protocol():
    # On ActorSystem config
    protocol_system_start(CigaretteSmoker)
    # Start the protocol
    prot = ProtocolMailbox.create(CigaretteSmoker, [A])
    prot[A].call.start()

