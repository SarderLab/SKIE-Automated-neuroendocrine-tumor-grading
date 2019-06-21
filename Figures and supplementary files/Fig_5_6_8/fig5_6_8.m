clc
clear all
close all

load algoAvg_GT_ImmRatio% algo avg, GT, IR 1st hs
load algo_8_hotspots % all 8 hotspots
load ImmRatio_5_hotspots
load Reg1
load Reg2
load Reg3

%% Fig - 5 ; Registration error 
Reg1 = Reg1.*100;
Reg2 = Reg2.*100;
Reg3 = Reg3.*100;

figure
x = [Reg1(1,:),Reg2(1,:),Reg3(1,:),...
    Reg1(2,:),Reg2(2,:),Reg3(2,:),...
    Reg1(3,:),Reg2(3,:),Reg3(3,:),...
    Reg1(4,:),Reg2(4,:),Reg3(4,:),...
    Reg1(5,:),Reg2(5,:),Reg3(5,:),...
    Reg1(6,:),Reg2(6,:),Reg3(6,:)];

group = [ones(1,5),2.*ones(1,5),3.*ones(1,5),4.*ones(1,5),5.*ones(1,5),6.*ones(1,5),...
    7.*ones(1,5),8.*ones(1,5),9.*ones(1,5),10.*ones(1,5),11.*ones(1,5),12.*ones(1,5),...
    13.*ones(1,5),14.*ones(1,5),15.*ones(1,5),16.*ones(1,5),17.*ones(1,5),18.*ones(1,5)];

positions = [1 1.25 1.5 2 2.25 2.5 3 3.25 3.5 4 4.25 4.5 5 5.25 5.5 6 6.25 6.5];
boxplot(x,group, 'positions', positions);

set(gca,'xtick',[mean(positions(1:3)) mean(positions(4:6)) mean(positions(7:9)) mean(positions(10:12))...
    mean(positions(13:15)) mean(positions(16:18)) ])
set(gca,'xticklabel',{'WSI-1','WSI-2','WSI-3','WSI-4','WSI-5','WSI-6'})

color = ['c', 'y', 'b', 'c', 'y','b','c', 'y','b', 'c', 'y','b','c', 'y', 'b','c', 'y','b'];
h = findobj(gca,'Tag','Box');
for j=1:length(h)
   patch(get(h(j),'XData'),get(h(j),'YData'),color(j),'FaceAlpha',.5);
end
% axis([0,7,0,0.2])
c = get(gca, 'Children');
hleg1 = legend(c(1:3), 'User 1', 'User 2', 'User 3' );
ylabel('Ki-67 proliferative index (%)')

%% Fig - 6
GT = algoAvg_GT_ImmRatio(:,2);
Avg_algo = mean(algo_8_hotspots(1:50,1:5),2).*100;
max_algo = max(algo_8_hotspots(1:50,1:5),[],2).*100;
figure;
mdl = fitlm(GT,Avg_algo)
plotResiduals(mdl,'caseorder','LineWidth',3)
axis([0,52,-25,25])

figure;
mdl = fitlm(GT,max_algo)
plotResiduals(mdl,'caseorder','LineWidth',3)
axis([0,52,-25,25])

Avg_ir = mean(ImmRatio_5_hotspots(1:50,1:5),2);
max_ir = max(ImmRatio_5_hotspots(1:50,1:5),[],2);
figure
mdlir = fitlm(GT,Avg_ir)
plotResiduals(mdlir,'caseorder','LineWidth',3)
axis([0,52,-25,25])

figure;
mdlir = fitlm(GT,max_ir)
plotResiduals(mdlir,'caseorder', 'LineWidth',3)
axis([0,52,-25,25])

%% Visualize curve
% Supplementary figure 4

figure;
curvex = 0:0.01:1

B = 5
Q = 1
v = 1.2
for i = 1:size(curvex,2)
    q = (2^Q);
    temp(:,i) = GenlogFn(curvex(i),B,q,v);    
end
curvey = temp';
plot(curvex,curvey,'k');
axis([0,1,0,1])


%% Fig - 8

load Errorsall % error bn gt and [path1 2 3 4 algoavg iravg]
figure;
h = boxplot(Errorsall, 'Widths',0.5)
set(h,{'linew'},{1.5})
set(gca,'xticklabel',{'P1','P2','P3','P4','Our method','ImmunoRatio'})

