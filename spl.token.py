import sys
from spl.token.client import Token
from solana.rpc.api  import Client
from spl.token.constants import TOKEN_PROGRAM_ID
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.exceptions import *
import info2 as stored_




class devnet_token:
    def __init__(self):
        '''
        initialize the class
        '''
        self.devnet_rpc="https://api.devnet.solana.com" #devnet rpc url
        self.client=Client(self.devnet_rpc)







    def generate_key(self):
        '''
        this method generates a key pair and stores it in a file named info2.py
        '''
        keys=Keypair()
        data=keys.to_json()
        with open("info2.py","w") as f:
            f.write(f'authority_key={data}')
            
            
            
            
            
            
    def airdrop_sol(self,):
        '''
        this method airdrops devnet sol to the pubkey that was genereated and stored in info2.py
        '''
        key=Keypair.from_bytes(stored_.authority_key)
        pub_key=key.pubkey()                                                                 #get the public key
        amount=int(input("Enter lamport amount  you want to request: "))                              # prompt theuser to enter the amount of sol needed in lamport
        if amount<=0:                                                                                    #check if the amount is positive
            print("Enter a positive amount ")
            self.airdrop_sol(key)
        else:
            try:                                                                           #try to request the sol from the  testnet rpc
                solamount=float(amount/1000000000)                                               #convert the lamport to amount
                print(f'you are requesting {solamount} SOL.....')
                self.request_sol=self.client.request_airdrop(pub_key,amount,)
                confirm=self.client.confirm_transaction(self.request_sol.value)
                print(f'{solamount}SOL has been airdroped successfully.......')
            except SolanaRpcException as e:                                                #exception handler
                print('Error: too many requests has been made \nTry again after some time',e)
                sys.exit(1)
                
        
        
        
        
        
    def create_mint_token(self):
        '''
        this method creates the token-mint ,associated token-account, and mint the created token to  the associated token account, 
        using the pubkey as the mint-authority of the mint and the owner of the associated token account.
        '''
        self.mint_authority=Keypair.from_bytes(stored_.authority_key)
        Owner=self.mint_authority.pubkey()
        
        print(f'Creating token......')
        token=Token.create_mint(self.client,                                                                  #create token mint
                                self.mint_authority,
                                self.mint_authority.pubkey(),
                                0,
                                TOKEN_PROGRAM_ID,
                                self.mint_authority.pubkey())
        print(f'successfully created the token <<{token.pubkey}>> \n')
        
        print('Creating associated token account......\n')
        token_account=Token.create_associated_token_account(token,                                          #create associated token account
                                                       Owner )
        print(f'The token account <<{token_account}>> has been successfully created\n')
     
     
        amount=int(input("Enter token amount  you want to request to mint to: "))                           # prompt theuser to enter the number of token that you want to mint
        if amount<=0:                                                                                       #check if the amount is positive
            print("TRY AGAIN:run the method again using a number > 0 ")
            sys.exit(1)
        else:
            amount=amount *(10**amount)          
        print(f'Minting {amount} tokens to the account {token_account}\n')     
        mint=token.mint_to(token_account,self.mint_authority,amount)                                        #mint the token to tha associated token account
        print(f'{amount} tokens has been successfully minted to the account {token_account}')
        print(Token.get_accounts_by_owner(token,Owner))
        
        
        
        
        
        
        
if __name__=='__main__':
    token=devnet_token()
    # token.generate_key()
    token.airdrop_sol()
    token.create_mint_token()