from cell.actors import Actor
from cell.roles import role, protocol, protocol_system_start, ProtocolMailbox
from cell.configuration import get_group_id, prot_config, get_num_from_id

c, DiningPhilosophers, Ph, A, n = "c", "DiningPhilosophers", "Ph", "A", 'n'

@protocol(c, DiningPhilosophers, Ph, [A], {Ph:n}, True)
class Philosopher(Actor):
    class state(Actor.state):
        @role(c)
        def join(self, c, cid):
            self.actor.join(cid=cid)
            self.roundsSoFar = 0
            self.num = get_num_from_id(self.actor.id)
            c.A.call.req(num=self.num)
            return True

        #@role(c)
        #def start(self, c):


        @role(c, A)
        def yes(self, c):
            self.eat()

        @role(c)
        def eat(self, c):
            self.roundsSoFar +=1
            c.A.call.done(num=self.num)

            if self.roundsSoFar < PhilConfig.rounds:
                c.A.call.req(num=self.num)
            else:
                c.A.call.exit()

        @role(c, A)
        def no(self, c):
            c.A.call.req(num=self.num)
			
@protocol(c, DiningPhilosophers, A, [Ph], {Ph:n})
class Arbitrator(Actor):
    class state(Actor.state):
        @role(c)
        def join(self, c, cid):
            self.actor.join(cid=cid)
            if not hasattr(self, 'forks') or not self.forks:
                self.init()
            return True

        def init(self):
            print 'Initialising'
            self.numExitedPhilosophers = 0
            self.forks = {}
            for i in range(0, PhilConfig.numForks):
                self.forks[i] = False

        @role(c, Ph)
        def req(self, c, num):
            if not hasattr(self, 'forks') or not self.forks:
                    self.init()

            leftFork = self.forks[num]
            rightFork = self.forks[num+1/ PhilConfig.numForks]

            if leftFork or rightFork:
                c.Ph[num].call.no()
            else:
                self.forks[leftFork] = False
                self.forks[rightFork] = False
                c.Ph[num].call.yes()

        @role(c, Ph)
        def done(self, c, num):
            leftFork = self.forks[num]
            rightFork = self.forks[num+1 / PhilConfig.numForks]
            self.forks[leftFork] = False
            self.forks[rightFork] = False

        @role(c, Ph)
        def exit(self, c):
            self.numExitedPhilosophers +=1
            if self.numExitedPhilosophers == PhilConfig.numForks:
                print 'The dinner is over!'

class PhilConfig:
    numForks = prot_config[DiningPhilosophers][n]
    rounds = 3

def start_protocol():
    # On ActorSystem config
    protocol_system_start(DiningPhilosophers)
    # Start the protocol
    ProtocolMailbox.create(DiningPhilosophers, [])

