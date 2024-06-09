from tokenizer import Tokenizer
import math
import numpy as np
from sklearn.linear_model import LinearRegression
import sys

class LM:
    
    def __init__(self):
        self.Total_Count_of_tokens=0
        self.freq_unigram={}
        self.freq_bigram={}
        self.freq_trigram={}
        self.unigram_probability={}
        self.bigram_probability={}
        self.trigram_probability={}
        self.Zr={}
        self.Zr_1={}
        self.b=None

    def train(self,filepath,type):
       
        token=cls.text_file(filepath)
        token=cls.identifiers_tokenizer(token)
        token=cls.sentence_tokenizer(token)
        token=cls.split_sentences_into_words(token)
        #print(token)
        self.Total_Count_of_tokens,self.freq_unigram,self.freq_bigram,self.freq_trigram,self.unigram_probability,self.bigram_probability,self.trigram_probability=cls.N_gram(token)
        if type=='g':
            with open('LM3_train-perplexity.txt', 'w',encoding='utf-8') as file:
                file.write("Sentence    Perplexity\n")

            perplexity=self.SGT(token,'train')
            print("Trained_perplexity:",perplexity)

            self.test(type)
        elif type=='i':
            # with open('LM4_train-perplexity.txt', 'w',encoding='utf-8') as file:
            #     file.write("Sentence    Perplexity\n")

            perplexity=self.linear_interpolation(token,'train',type)
            print("Trained_perplexity:",perplexity)
            self.test(type)

    def test(self,type):
        test_sentence=input("Enter file path")
        token=cls.text_file(test_sentence)
        token=cls.identifiers_tokenizer(token)
        token=cls.sentence_tokenizer(token)
        token=cls.split_sentences_into_words(token)

        if type=='g':
            with open('LM3_test-perplexity.txt', 'w',encoding='utf-8') as file:
                file.write("Sentence    Perplexity\n")
            perplexity=self.SGT(token,'test')
    
            print("Test_perplexity:",perplexity)

        elif type=='i':
           
            # with open('LM4_test-perplexity.txt', 'w',encoding='utf-8') as file:
            #     file.write("Sentence    Perplexity\n")

            perplexity=self.linear_interpolation(token,'test',type)
        
            print("Test_perplexity:",perplexity)
            
    def trigram_bigram_unigram_creation(self,i,j):
        if j==0:
            trigram=('<s>','<s>',i[j])
            bigram=('<s>',i[j])
                  
                  
        elif j==1:
            trigram=('<s>',i[j-1],i[j])
            bigram=(i[j-1],i[j])
            
            
        else:
            trigram=(i[j-2],i[j-1],i[j])
            bigram=(i[j-1],i[j])
        
        
        unigram=(i[j])

        return trigram,bigram,unigram

    def lambda_calculation(self):
        lambda1=0;lambda2=0;lambda3=0
        #print(self.freq_trigram)
        for key,val in self.freq_trigram.items():
           
            t1t2=key[0:2]
            t2t3=key[1:]
            t3=key[2]
            t2=key[1]
           # print(key,t1t2,t2t3,t3,t2)
            if self.freq_bigram[t1t2]==1:
                c1=0
            else:
                c1=(val-1)/(self.freq_bigram[t1t2]-1)
            if self.freq_unigram[t2]==1:
                c2=0
            else:
                c2=(self.freq_bigram[t2t3]-1)/(self.freq_unigram[t2]-1)
            c3=(self.freq_unigram[t3]-1)/(self.Total_Count_of_tokens-1)
       
            if c1>=c2 and c1>=c3:
                lambda1=lambda1+val
            elif c2>=c1 and c2>=c3:
                lambda2=lambda2+val
            else:
                lambda3= lambda3+val

        return lambda1,lambda2,lambda3
    
    def perplexity(self,prob_of_sen,no_of_tri):
        t=prob_of_sen/no_of_tri*(-1)
         
        perplexity_of_each_sentence=math.exp(t)
        #print("PErplexity of each sen:",perplexity_of_each_sentence)
        return perplexity_of_each_sentence
    
    def linear_interpolation(self,tokens,type,LM_model):
        final_perplexity=0
        lambda1,lambda2,lambda3=self.lambda_calculation()
        lambda1,lambda2,lambda3=lambda1/(lambda1+lambda2+lambda3),lambda2/(lambda1+lambda2+lambda3),lambda3/(lambda1+lambda2+lambda3)
        for i in tokens:
           
            prob_of_each_trigram=0
            for j in range(len(i)):
                trigram,bigram,unigram=self.trigram_bigram_unigram_creation(i,j)
               

                temp=lambda1*self.unigram_probability.get(unigram, 0)+lambda2*self.bigram_probability.get(bigram,0)+lambda3*self.trigram_probability.get(trigram,0)
                if temp==0:
                    temp=0.00001
              
                prob_of_each_trigram=prob_of_each_trigram+math.log(temp)

            print("Probability of each sentence:",math.exp(prob_of_each_trigram))

            perplexity_of_each_sentence=self.perplexity(prob_of_each_trigram,len(i))
            final_perplexity=final_perplexity+perplexity_of_each_sentence
           
        
            # if type == 'test':
            #     with open('LM4_test-perplexity.txt', 'a',encoding='utf-8') as file:
            #         # Append content to the file
            #         file.write(str(i)+"  "+str(perplexity_of_each_sentence)+"\n")
            # else:
                
            #     with open('LM4_train-perplexity.txt', 'a',encoding='utf-8') as file:
            #         # Append content to the file
            #         file.write(str(i)+"  "+str(perplexity_of_each_sentence)+"\n")
        

        
        return final_perplexity/len(tokens)
        
    def Std_Deviation(self,r,Nr,Nr_1):
        var=math.pow(r+1,2)*(Nr_1/(Nr**2))*(1+(Nr_1/Nr))
        return math.sqrt(var)
    
    def Turing_Estimate(self,r,Nr,Nr_1):
        r_ast=(r+1)*Nr_1/Nr
        return r_ast
    
    def Good_Turing_Estimate(self,r,b):
        r_ast=r*math.pow((1+1/r),(b+1))
        return r_ast
    
    def Zr_estimation_with_b(self):
        sorted_trigram = dict(sorted(self.freq_trigram.items(), key=lambda x: x[1]))
        Nr_dict={}
        
        for key,value in sorted_trigram.items():
            Nr_dict[value]=Nr_dict.get(value,0) + 1

        key=list(Nr_dict.keys())
        val=list(Nr_dict.values())
        # print(key)
        # print(val)
        for i in range(len(val)):
            if  key[i]==key[0] and key[i]==key[len(key)-1]:
                self.Zr[key[i]]=val[i]
            elif key[i]==key[0]:
                self.Zr[key[i]]=val[i]/0.5*key[i+1]
            elif key[i]==key[len(key)-1]:
                self.Zr[key[i]]=val[i]/(key[i]-key[i-1])
            else:
                self.Zr[key[i]]=val[i]/0.5*(key[i+1]-key[i-1])

        for i in range(len(key)):
            if i==len(key)-1:
                self.Zr_1[key[i]]=self.Zr[key[i]]
            else:
                self.Zr_1[key[i]]=self.Zr[key[i+1]]

        value=list(self.Zr.values())
        key=list(self.Zr.keys())
        # print("key:",key)
        # print("value:",value)
        self.b=self.linear_reg(key,value)

        
  
    def linear_reg(self,key,val):
        

        
        X=np.array([math.log(r) for r in key]).reshape(-1,1)
        y=np.array([math.log(N_r) for N_r in val]).reshape(-1,1)

        model=LinearRegression()
        model.fit(X,y)
        b=model.coef_[0][0]
        #print("B:",b)#2.3
        return b
        
    def Count_of_denominator(self,bigram):
        total_r_ast=0
        for key,values in self.freq_unigram.items():
            #print(bigram)
            new_trigram=bigram+(key,)
           # print("New trigram",new_trigram)
            total_r_ast+=self.calculation(new_trigram)
        #print(total_r_ast)
        return total_r_ast
    


    def calculation(self,trigram):
        if trigram in self.freq_trigram:
           # print("Inside the trigram")
            r=self.freq_trigram[trigram]
            S_Nr=self.Zr[r]
            S_Nr_1=self.Zr_1[r]
            std_deviation=self.Std_Deviation(r,S_Nr,S_Nr_1)
            turing_estimate=self.Turing_Estimate(r,S_Nr,S_Nr_1)
            goog_turing_estimate=self.Good_Turing_Estimate(r,self.b)
            check=turing_estimate-goog_turing_estimate
            #have to modify it as ind=r if check satisfies
            if check>1.65*std_deviation:
                r_ast=goog_turing_estimate #need to check because control should got to gte after statement is true
            else:
                r_ast=turing_estimate
        else:
            r_ast=0

        return r_ast
    
    def SGT(self,token,type):
     
        self.Zr_estimation_with_b()
        
        
        overall_preplexity=0
        for i in token:
            #print("Sentence",i)
            prob_of_sentence=0
            for j in range(len(i)):
                trigram,bigram,unigram=self.trigram_bigram_unigram_creation(i,j)
                num_count=self.calculation(trigram)
                bigram=trigram[0:2]
                if num_count==0:
                    t=0.00001
                else:
                    count_of_denominator=self.Count_of_denominator(bigram)
                    t=num_count/count_of_denominator
                prob_of_sentence+=math.log(t)
            #print("Probability of each sentence:",math.exp(prob_of_sentence))
            perplexity_of_each_sentence=self.perplexity(prob_of_sentence,len(i))
            overall_preplexity+=perplexity_of_each_sentence

            
            if type == 'test':
                with open('LM3_test-perplexity.txt', 'a',encoding='utf-8') as file:
                    # Append content to the file
                    file.write(str(i)+"  "+str(perplexity_of_each_sentence)+"\n")
            else:
                
                with open('LM3_train-perplexity.txt', 'a',encoding='utf-8') as file:
                    # Append content to the file
                    file.write(str(i)+"  "+str(perplexity_of_each_sentence)+"\n")
           
                
        overall_preplexity=overall_preplexity/len(token)
        return overall_preplexity
       



type=sys.argv[1]
path = sys.argv[2]

# file_path=input("Enter filepath: ")
cls=Tokenizer()
lm_cls=LM()
# type=input("Type:")
lm_cls.train(path,type)


