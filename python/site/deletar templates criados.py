import os
from posixpath import splitext
import shutil
path=r'./src/Components/pages/imoveis/'
list_path=[]

for root,dirs,files in os.walk(path):
    for file in files:
        list_path.append(os.path.join(root,file))
for name in list_path:
    print(name)

list_available=[]

# listar todos os imoveis
for root, dirs, files in os.walk(r'./src/Components/pages/imoveis/'):
    for filename in files:
        list_available.append(filename)
j=0 
for i in list_available:
    print(j,i)
    j=j+1

escolha=int(input('Escolha o numero do imovel: '))
while(True):
    if escolha>=0 and escolha<=j-1:
        file_to_delete_path=list_path[escolha]
        if os.path.isfile(file_to_delete_path):
            os.remove(file_to_delete_path)
            print('foi deletado a pagina do imovel: ',list_available[escolha])
        else:
            print('o arquivo %s para deletar nao existe'%file_to_delete_path)

        print('deletando fotos')

        if os.path.isdir('./src/assets/imoveis/'+  splitext(list_available[escolha])[0]):
            shutil.rmtree('./src/assets/imoveis/'+  splitext(list_available[escolha])[0])
        else:
            print('arquivos de fotos nao existem')
        
        list_to_delete_in_indexjs=[]
        list_to_delete_in_indexjs.append(splitext(list_available[escolha])[0])
        with open("./src/App.js", "r") as input:
            with open("temp.txt", "w") as output:
                # iterate all lines from file
                for line in input:
                    # if substring contain in a line then don't write it
                    if list_to_delete_in_indexjs[0] not in line.strip("\n"):
                        output.write(line)

        # replace file with original name
        os.replace('temp.txt', './src/App.js')
        print('deletado imovel do app.js')

        with open('./src/Components/pages/Imoveis.jsx','r',encoding='utf-8') as input:
            with open('temp.txt','w',encoding='utf-8') as output:
                for line in input:
                    if list_to_delete_in_indexjs[0] not in line.strip('\n'):
                        output.write(line)
        os.replace('temp.txt','./src/Components/pages/Imoveis.jsx')
        print('deletado o link do index')
        exit()
    else:
        escolha=int(input('Escolha o numero do imovel, denovo: '))