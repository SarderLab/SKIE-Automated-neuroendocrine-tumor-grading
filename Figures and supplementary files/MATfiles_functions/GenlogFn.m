function Y = GenlogFn(t,B,Q,v)

A = 0;
C = 1;
K = 1;

Y = A + ((K-A) / ((C+Q*exp(-B*t)).^(1/v)));

end