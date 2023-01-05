# Script Name     : oddevensort.py
# Author          : Super Bitch
# Created         : 5th Jan 2023
# Last Modified	  : 5th Jan 2023
# Version         : 0.114514
# Modifications	  : 
# Description     : Odd-Even sorting algorithm.

import copy
from .data import Data

def oddeven_sort(data_set):
    # FRAME OPERATION BEGIN
    frames = [data_set]
    # FRAME OPERATION END
    ds = copy.deepcopy(data_set)
    for phase in range(0, Data.data_count):
        if phase % 2 == 1: # ODD PHASE
            for i in range(1, Data.data_count-1, 2):
                #FRAME OPERATION BEGIN
                ds_r = copy.deepcopy(ds)
                frames.append(ds_r)
                ds_r[i].set_color('r')
                ds_r[phase].set_color('k')
                ds_r[i+1].set_color('pink')                
                #FRAME_OPERATION END
                if ds[i].value > ds[i+1].value:
                    ds[i], ds[i+1] = ds[i+1], ds[i]
        else: # EVEN PHASE
            for i in range(1, Data.data_count, 2):
                #FRAME OPERATION BEGIN
                ds_r = copy.deepcopy(ds)
                frames.append(ds_r)
                ds_r[i].set_color('r')
                ds_r[phase].set_color('k')
                ds_r[i-1].set_color('pink')
                #FRAME_OPERATION END
                if ds[i-1].value > ds[i].value:
                    ds[i-1], ds[i] = ds[i], ds[i-1]
        

    # FRAME OPERATION BEGIN
    frames.append(ds)
    return frames
    # FRAME OPERATION END
    
    
def para_oddeven_sort(data_set):
    # FRAME OPERATION BEGIN
    frames = [data_set]
    # FRAME OPERATION END
    
    
    # LOCAL SPLIT_MERGE SORT
    def split_merge(ds,head,tail,frames):
        mid = (head + tail) // 2
        if tail - head > 2:
            split_merge(ds,head,mid,frames)
            split_merge(ds,mid,tail,frames)
        #FRAME OPERATION BEGIN
        ds_yb = copy.deepcopy(ds)
        for i in range(head, mid):
            ds_yb[i].set_color('y')
        for i in range(mid, tail):
            ds_yb[i].set_color('b')
        #FRAME OPERATION END
        left = head
        right = mid
        tmp_list = []
        for i in range(head, tail):
            # FRAME OPERATION BEGIN
            frames.append(copy.deepcopy(ds_yb))
            # FRAME OPERATION END
            if right == tail or (left < mid and ds[left].value <= ds[right].value):
                tmp_list.append(ds[left])
                # FRAME OPERATION BEGIN
                frames[-1][left].set_color('r')
                # FRAME OPERATION END
                left += 1
            else:
                tmp_list.append(ds[right])
                # FRAME OPERATION BEGIN
                frames[-1][right].set_color('r')
                # FRAME OPERATION END
                right += 1
        for i in range(head, tail):
            ds[i] = tmp_list[i-head]
        # FRAME OPERATION BEGIN
        frames.append(copy.deepcopy(ds))
        # FRAME OPERATION END
    
    # THREAD MERGE 
    def thread_merge(ds,thread1,thread2):   
        ds_yb = copy.deepcopy(ds)
        frames = []
        for i in range(Lid[thread1],Lid[thread1]+local_length_list[thread1]):
            ds_yb[i].set_color('g')
        for i in range(Lid[thread2],Lid[thread2]+local_length_list[thread2]):
            ds_yb[i].set_color('pink')
        
        # Get Thread with smaller id and greater id.
        threadL = min(thread1,thread2)
        threadR = max(thread1,thread2)
        
        # threadL keeps smaller keys. threadR keeps greater keys.
        # pointer in threadL goes from left to right
        # pointer in threadR goes from right to left
        # threadL and threadR fetch data at the same pace
        # iteration for threadL goes from Lid[threadL] to Lid[threadL]+local_length_list[threadL]-1
        # iteration for threadR goes from Lid[threadR]+local_length_list[threadR]-1 to Lid[threadR]
        max_ptr_iters = max(local_length_list[threadL],local_length_list[threadR])
        threadL_iter_start = Lid[threadL]
        threadL_iter_end = Lid[threadL]+local_length_list[threadL]-1
        threadR_iter_start = Lid[threadR]+local_length_list[threadR]-1
        threadR_iter_end = Lid[threadR]
        threadL_length = threadL_iter_end - threadL_iter_start + 1
        threadR_length = threadR_iter_start - threadR_iter_end + 1
        
        # Fetching ptrs
        threadL_fetchL = threadL_iter_start
        threadL_fetchR = threadR_iter_end
        threadR_fetchL = threadL_iter_end
        threadR_fetchR = threadR_iter_start
        threadL_list = []
        threadR_list = []
        
        # get pointer iterations in threadL and threadR
        for i in range(max_ptr_iters):
            frames.append(copy.deepcopy(ds_yb))
            frames[-1][threadL_fetchL].set_color('r')
            frames[-1][threadL_fetchR].set_color('b')
            frames[-1][threadR_fetchR].set_color('r')
            frames[-1][threadR_fetchL].set_color('b')
            
            # *** Avoid Repetitive Pick ***
            if len(threadL_list) < threadL_length:
                if threadL_fetchL > threadL_iter_end and threadL_fetchR <= threadR_iter_start:
                    threadL_list.append(ds_yb[threadL_fetchR])
                    threadL_fetchR += 1
                elif threadL_fetchL <= threadL_iter_end and threadL_fetchR > threadR_iter_start:
                    threadL_list.append(ds_yb[threadL_fetchL])
                    threadL_fetchL += 1    
                elif threadL_fetchL > threadL_iter_end and threadL_fetchR > threadR_iter_start:
                    pass
                else:
                    if ds_yb[threadL_fetchL].value > ds_yb[threadL_fetchR].value:
                        threadL_list.append(ds_yb[threadL_fetchR])
                        threadL_fetchR += 1
                    else: 
                        threadL_list.append(ds_yb[threadL_fetchL])
                        threadL_fetchL += 1
            
            if len(threadR_list) < threadR_length:
                if threadR_fetchL < threadL_iter_start and threadR_fetchR >= threadR_iter_end:
                    threadR_list.append(ds_yb[threadR_fetchR])
                    threadR_fetchR -= 1
                elif threadR_fetchL >= threadL_iter_start and threadR_fetchR < threadR_iter_end:
                    threadR_list.append(ds_yb[threadR_fetchL])
                    threadR_getchL -= 1
                elif threadR_fetchL < threadL_iter_start and threadR_fetchR < threadR_iter_end:
                    pass
                else:   
                    if ds_yb[threadR_fetchL].value >= ds_yb[threadR_fetchR].value:
                        threadR_list.append(ds_yb[threadR_fetchL])
                        threadR_fetchL -= 1
                    else:
                        threadR_list.append(ds_yb[threadR_fetchR])
                        threadR_fetchR -= 1
                        
        threadR_list.reverse()
        
        # Write the result back to ds
        ds_a = copy.deepcopy(ds)
        tot_list = threadL_list + threadR_list
        for i in range(Lid[threadL],Lid[threadR]+local_length_list[threadR]):
            ds_a[i] = tot_list[i-Lid[threadL]]
            ds_a[i].set_color()
        frames.append(ds_a) 
        return frames           
                
    
    
    
    
    # Determining the Amount of Local Job
    thread_count = 8 # Change this value if needed.
    local_length = Data.data_count // thread_count
    local_length_list = []
    residue = Data.data_count % thread_count
    for i in range(thread_count):
        if(residue > 0):
            local_length_list.append(local_length+1)
            residue -= 1
        else:
            local_length_list.append(local_length)
    Lid = [sum(local_length_list[0:i]) for i in range(thread_count)]


    #------ SORT LOCAL KEYS ------
    
    # Get Local Sorting Steps
    thread_frames = []
    for i in range(thread_count):
        thread_frames.append([])
        ds_each_thread = copy.deepcopy(data_set)
        split_merge(ds_each_thread,Lid[i],Lid[i]+local_length_list[i],thread_frames[i])

    # Combine Local Sorting Steps
    frame_cnt_local_sort = max([len(thread_frames[i]) for i in range(thread_count)])
    for i in range(frame_cnt_local_sort):
        cur_frame = []
        for j in range(thread_count):
           cur_frame += thread_frames[j][min(i,len(thread_frames[j])-1)][Lid[j]:Lid[j]+local_length_list[j]]
        frames.append(cur_frame)
    
    #------ ODD EVEN SWAP ------
    
    # Odd-even thread merge
    ds = frames[-1]
    
    for phase in range(thread_count): 
        ds = frames[-1]
#        thread_frames = []
#        for i in range(thread_count):
#            thread_frames.append([])
        if phase % 2 == 1: # ODD PHASE
            ds_each_thread = copy.deepcopy(ds)
            for i in range(1,thread_count-1,2):
                thread_frames[i]=thread_merge(ds_each_thread,i,i+1)
            # Merge the Thread_merge results
            frame_cnt_merge = max([len(thread_frames[i]) for i in range(1,thread_count-1,2)])       
            for i in range(frame_cnt_merge):
                cur_frame = []
                cur_frame += ds[0:Lid[1]] # SPECIAL JUDGE
                for j in range(1,thread_count-1,2):
                    cur_frame += thread_frames[j][min(i,len(thread_frames[j])-1)][Lid[j]:Lid[j+1]+local_length_list[j+1]]
                cur_frame += ds[len(cur_frame):]
                frames.append(cur_frame)

        else: # EVEN PHASE
            ds_each_thread = copy.deepcopy(ds)
            for i in range(1,thread_count,2):
                thread_frames[i]=thread_merge(ds_each_thread,i,i-1)
            # Merge the Thread_merge results
            frame_cnt_merge = max([len(thread_frames[i]) for i in range(1,thread_count,2)])       
            for i in range(frame_cnt_merge):
                cur_frame = []   
                for j in range(1,thread_count,2):
                    cur_frame += thread_frames[j][min(i,len(thread_frames[j])-1)][Lid[j-1]:Lid[j]+local_length_list[j]]
                cur_frame += ds[len(cur_frame):]
                frames.append(cur_frame)
             
    ds = frames[-1]
    
    # FRAME OPERATION BEGIN
    frames.append(ds)
    return frames
    # FRAME OPERATION END
    