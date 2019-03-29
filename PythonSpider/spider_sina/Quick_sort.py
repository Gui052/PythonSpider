'''
Created on 2017年7月16日

@author: aaron
'''
import random
def Quick_sort(A,p,r):
    if p<r:
        q=partition(A, p, r)
        Quick_sort(A, p,q-1)
        Quick_sort(A, q+1, r)
    return A
def partition(A,p,r):
    i=p-1
    for j in range(p,r):
        if A[j]>=A[r]:
            i+=1
            temp=A[j]
            A[j]=A[i]
            A[i]=temp  
    temp1=A[i+1]
    A[i+1]=A[r]
    A[r]=temp1
    return i+1  
def Rand_partition(A,p,r):
    c=random.randint(p,r)
    temp3=A[c]
    A[c]=A[r]
    A[r]=temp3
    i=p-1
    for j in range(p,r):
        if A[j]>=A[r]:
            i+=1
            temp=A[j]
            A[j]=A[i]
            A[i]=temp  
    temp1=A[i+1]
    A[i+1]=A[r]
    A[r]=temp1
    return i+1  
if __name__ == '__main__':
    A=[10,12,13,15,6,8,19,6,2,5,14,18]
    p=0
    r=len(A)-1
    print(Quick_sort(A, p, r))