from tokenizer import Tokenizer
import sys

class Generator:

    def __init__(self):
        self.Total_Count_of_tokens=0
        self.freq_unigram={}
        self.freq_bigram={}
        self.freq_trigram={}
        self.unigram_probability={}
        self.bigram_probability={}
        self.trigram_probability={}

    def tokenizer_for_corpus(self,file_path,k):
        token=cls.text_file(file_path)
        token=cls.identifiers_tokenizer(token)
        token=cls.sentence_tokenizer(token)
        token=cls.split_sentences_into_words(token)
        self.Total_Count_of_tokens,self.freq_unigram,self.freq_bigram,self.freq_trigram,self.unigram_probability,self.bigram_probability,self.trigram_probability=cls.N_gram(token)
        
        input_sen=(input("Enter sentence :"))
        #n=int(input("Enter N"))
        #count=n-1
        count=3 #for LM generation
        s=""
        j=len(input_sen)
        for i in range(len(input_sen)-1,0,-1):
            if input_sen[i]==" " and count>0:
                count-=1
                s=input_sen[i:j]+s
                j=i
        #print(s)
        tokenise_sen=cls.identifiers_tokenizer(s)
        token=cls.sentence_tokenizer(tokenise_sen)
        bigram=cls.split_sentences_into_words(token)
        print(bigram[0])
        #self.n_gram_generator(bigram[0],k)
        self.LM_generator(bigram[0],k)

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

    def n_gram_generator(self,bigram,k):
        predicted_wor_prob={}
        for key_,v in self.freq_unigram.items():
            new_trigram=tuple(bigram)+(key_,)
            predicted_wor_prob[key_]=self.bigram_probability.get(new_trigram,0)
            
        self.print_k(k,predicted_wor_prob)

    def LM_generator(self,bigram,k):
        predicted_wor_prob={}
        lambda1,lambda2,lambda3=self.lambda_calculation()
        lambda1,lambda2,lambda3=lambda1/(lambda1+lambda2+lambda3),lambda2/(lambda1+lambda2+lambda3),lambda3/(lambda1+lambda2+lambda3)
        
        for key_,v in self.freq_unigram.items():
            new_trigram=tuple(bigram)+(key_,)
            new_bigram=new_trigram[1:]
            new_unigram=key_
            temp=lambda1*self.unigram_probability.get(new_unigram, 0)+lambda2*self.bigram_probability.get(new_bigram,0)+lambda3*self.trigram_probability.get(new_trigram,0)
            predicted_wor_prob[key_]=temp

        self.print_k(k,predicted_wor_prob)

    

    def print_k(self,k,predicted_wor_prob):
        sorted_trigram = dict(sorted(predicted_wor_prob.items(), key=lambda x: x[1], reverse=True))
        key=list(sorted_trigram.keys())
        for i in range(k):
            print(key[i]," ",sorted_trigram[key[i]])

cls=Tokenizer()


gen_cls=Generator()

path = sys.argv[1]
k=int(sys.argv[2])
gen_cls.tokenizer_for_corpus(path,k)

