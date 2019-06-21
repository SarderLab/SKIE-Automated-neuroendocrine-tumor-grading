clc
close all
clear all

%% range of parameters
Qmax = 60;
Qinc = 10;
Qlow = 1;
vmax = 2 ;
vinc = 0.1;
vlow = 0.1;
Bmax = 50;
Binc = 1;
B_low = 5;

%% Error estimation

count = 1;
for v = vlow:vinc:vmax
    for Q = Qlow:Qinc:Qmax
        for B = B_low:Binc:Bmax
            q = 2^Q;
            F(1:3,count) = [B;q;v];            
           [F(4,count),F(5,count)] = myfun2([B;q;v]);
            count = count +1
        end
    end
end
save F F