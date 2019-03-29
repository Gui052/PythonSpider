'''
Created on 2017年7月15日

@author: aaron
'''
def MAX_h(A,i):
    temp1=0
    temp2=0
    l=left(i)
    r=right(i)
    if A[l]>A[i] and l<len(A):
        temp1=A[l]
        A[l]=A[i]
        A[i]=temp1  
        largest=l
    else:
        largest=i
    if A[r]>A[i] and r<len(A):
        temp2=A[r]
        A[r]=A[i]
        A[i]=temp2  
        largest=r 
    else:
        largest=i
    if i==0:
        return A,largest
    return MAX_h(A,i-1)
def left(i):
    l=0
    l=2*i+1
    return l

def right(i):
    r=0
    r=2*i+2
    return r

if __name__ == '__main__':
    global largest
    largest=0
    A=[3,5,7,9,8,16,13,17,15,45,2]
    c=len(A)
    while c>=2:
          i=int(c/2)-1
          if c==len(A):
             A=MAX_h(A, i)
          else:
             A = [x for x in A if x==A[0]]
             A=MAX_h(A, i)
          c=c-1
    print(A)
          
          
        
    
          
          
          