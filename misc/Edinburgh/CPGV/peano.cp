type Peano = mu X.+{zero: 1, succ: X}.

def Zero(x) = rec x.x/zero.x[].0.
check Zero(x) |- x:Peano.

def Inc(x,y) = rec y.y/succ.y<->x.
check Inc(x,y) |- x:~Peano,y:Peano.

def Two(x) = new [y:Peano] (new [z:Peano] (Zero(z) | Inc(z,y)) | Inc(y,x)).

def Add(x,y,z) =
  corec x [a:Peano*~Peano]
    (a[y0].(y <-> y0 | a <-> z),
     a(b).case x {zero: x().a<->b;
                  succ: x[b0].(Inc(b,b0) | a<->x)}).
check Add(x,y,z) |- x:~Peano,y:~Peano,z:Peano.

def Count(x,y) =
  corec x [z:int || bot]
   (y<->z,
    case x { zero: x().z*[0].z[].0;
             succ: x*(i).x().z*[i + 1].z[].0 }).

new [z:Peano] (new [x:Peano] (Two(x) | new [y:Peano] (Two(y) | Add(x,y,z))) | Count(z,a)) |- a:int*1.