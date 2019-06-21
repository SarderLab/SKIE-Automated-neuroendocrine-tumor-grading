function [F,errorRate] = myfun2(x)
load newHSdata
load GT
for slide_no = 1:45
    
    clear NumBrownCellsPerHS NumBlueCellsPerHS
    clear algoKi67indxPerHS N algoKi67indxPerHS
    clear weightedIDX_beforeNorm NewWeightsPerFunction NumBlueCellsPerHS
    % slide_no =22;
    N = newHSdata(slide_no).details;
    
    NumBrownCellsPerHS=N(:,3); % #br
    NumBrownCellsPerHS=NumBrownCellsPerHS./max(NumBrownCellsPerHS); % get 0 or 0.-- to 1 prior to sigmoid curve
    NumBlueCellsPerHS = N(:,4);
    algoKi67indxPerHS =N(:,5);
    algoKi67indxPerHS = algoKi67indxPerHS.*100; % % of index

        for i = 1:size(NumBrownCellsPerHS,1)
    
            NewWeightsPerFunction(i) = 1 / ((1+(x(2)*exp(-x(1)*NumBrownCellsPerHS(i)))).^(1/x(3)));
    
        end
    
    
    weightedIDX_beforeNorm = NewWeightsPerFunction'.*algoKi67indxPerHS;
    Sum_of_New_weights = sum(NewWeightsPerFunction);
    
    weightedIDX_afterNorm  = (sum(weightedIDX_beforeNorm))/Sum_of_New_weights;
    
    estWSIidx_perslide(slide_no,:) = weightedIDX_afterNorm;

end

GT_grade = GT(1:45);
GT_grade(GT_grade<2.5) = 1;
GT_grade(GT_grade>2.5) = 2;

EstimatedGrades = estWSIidx_perslide;
EstimatedGrades(EstimatedGrades<2.5) = 1;
EstimatedGrades(EstimatedGrades>2.5) = 2;

F = sum(GT_grade == EstimatedGrades);
errorRate = mse(estWSIidx_perslide,GT(1:45));
