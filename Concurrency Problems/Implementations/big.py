from cell.actors import Actor
from cell.roles import role, protocol, protocol_system_start, ProtocolMailbox

#my_app = celery.Celery(broker='pyamqp://guest@localhost//')
#agent = dAgent(connection=my_app.broker_connection())
c, Big, A, B, S = 'c', 'Big', 'A', 'B', 'S'

@protocol(c, Big, B, [A, S])
class Pong(Actor):	
    class state(Actor.state):
        @role(c)
        def join(self, c, cid):
            self.actor.join(cid=cid)
            c.A.call.ping()

        @role(c, A)
        def ping(self, c):
            c.A.call.pong()

        @role(c, A)
        def pong(self, c):
            c.S.call.done()

        @role(c, S)
        def done(self, c):
            print 'Pong is done.'

@protocol(c, Big, A, [B, S])
class Ping(Actor):
    class state(Actor.state):
        @role(c)
        def join(self, c, cid):
            self.actor.join(cid=cid)
            c.B.call.ping()

        @role(c, B)
        def ping(self, c):
            c.B.call.pong()

        @role(c, B)
        def pong(self, c):
            c.S.call.done()

        @role(c, S)
        def done(self, c):
            print 'Ping is done'

@protocol(c, Big, S, [A, B])
class Sink(Actor):
    class state(Actor.state):
        @role(c)
        def join(self, c, n):
            self.actor.join(cid=cid)
            print 'In join'
            return True

        @role(c)
        def start(self, c, n):
            self.n = n

        @role(c)
        def done(self, c):
            print 'In done and n is', self.n
            if self.n <=1:
                c.A.call.done()
                c.B.call.done()
                print "The sink is done"
            else: self.n=self.n-1


def start_protocol():
    # On ActorSystem config
    protocol_system_start(Big)
    # Start the protocol
    prot = ProtocolMailbox.create(SleepingBarber, [S])
    # Initiate the first action
    prot[S].call.start(n=2)


