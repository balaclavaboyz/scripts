def give_only_ref():
    import pandas
    import codecs
    import os
    import re

    if os.path.getsize('temp') == 0:
        list_local_files=[]
        list_imoveis_only_file=[]
        for path in os.listdir('./'):
            if os.path.isfile(os.path.join('./',path)):
                list_local_files.append(path)
        for i in list_local_files:
            if re.search(r'^imovel',i):
                list_imoveis_only_file.append(i)
        j=0
        while(True):
            for i in list_imoveis_only_file:
                print(j,i)
                j=j+1
            escolha=int(input('Escolha o numbero do arquivo: '))
            if escolha >=0 and escolha <=j-1:
                nome_arquivo_csv=list_imoveis_only_file[escolha]
                break
            else:
                escolha=input('Escolha o arquivo csv: ')

        with open('temp','w') as f:
            f.write(nome_arquivo_csv)
    else:
        with open('temp','r') as f:
            nome_arquivo_csv = f.read()

    BLOCKSIZE = 1048576  # or some other, desired size in bytes
    with codecs.open(nome_arquivo_csv, "r", "ISO-8859-1") as sourceFile:
        with codecs.open('temp.csv', "w", "utf-8") as targetFile:
            while True:
                contents = sourceFile.read(BLOCKSIZE)
                if not contents:
                    break
                targetFile.write(contents)

    csv = pandas.read_csv('temp.csv', encoding='utf-8', sep=';')
    return(csv)


def csv_to_page():
    import codecs

    csv = give_only_ref()

    ref = csv['Referência'].loc[csv.index[0]]
    titulo = csv['Título'].loc[csv.index[0]]
    endereco = csv['Endereço'].loc[csv.index[0]]
    finalidade = csv['Finalidade'].loc[csv.index[0]]
    valor_locacao = csv['Valor Locação'].loc[csv.index[0]]
    valor_venda = csv['Valor Venda'].loc[csv.index[0]]
    descricao = csv['Descrição'].loc[csv.index[0]]
    endereco_googlemaps = endereco.replace(" ", "%20")

    file_path = './src/Components/pages/imoveis/' + ref + '.jsx'

    blob_of_text = ("import React from \"react\";import InnerHTML from \"dangerously-set-html-content\";export default function "+ref+"() {function importAll(r) {let images = {};r.keys().forEach((item, index) => {images[item.replace(\"./\", \"\")] = r(item);});return images;}const imgs = importAll(require.context(`../../../assets/imoveis/"+ref+"`,false,/\.(png|jpe?g|svg|webp)$/));const googleMaps = `<div class=\"mapouter\"><div class=\"gmap_canvas\"><iframe src=\"https://maps.google.com/maps?q="+endereco_googlemaps +
                    "&amp;t=&amp;z=18&amp;ie=UTF8&amp;iwloc=&amp;output=embed\" id=\"gmap_canvas\" frameborder=\"0\" scrolling=\"no\" style=\"width: 600px; height: 400px;\"></iframe><style>.mapouter{position:relative;text-align:right;height:400px;width:600px;}</style><a href=\"https://googlemapsiframegenerator.com\" style=\"display:none\">Google Maps Iframe Generator - Free Html Embed Code</a><style>.gmap_canvas{overflow:hidden;background:none!important;height:400px;width:600px;}</style></div></div>`;return (<><div className=\"container_imoveis_menu container\"><div className=\"imoveis_context\"><div className=\"imovelGaleria\"><div className=\"imoveis_imgs\">{Object.entries(imgs).map((t, k) => (<div key={k}><a href={t[1]} target=\"_blank\" rel=\"noopener noreferrer\"><img src={t[1]} alt=\"test\" /></a></div>))}</div><div className=\"imoveis_desp\"><hr /><h1>"+titulo+"</h1><p>"+endereco+"</p><p>Finalidade: "+finalidade+"</p><p>Valor da Locação: "+valor_locacao+"</p><p>Valor da Venda: "+valor_venda+"</p><hr /><h2>Descrição</h2><p>"+descricao+"</p><hr /><InnerHTML className=\"center\" html={googleMaps}></InnerHTML></div></div></div></div></>);}")

    with codecs.open(file_path, "w", "utf-8-sig") as temp:
        temp.write(blob_of_text)

    # opening a text file
    file1 = open('./src/app.js', "r")

    # read file content
    readfile = file1.read()

    # checking condition for string found or not
    if ref in readfile:
        print(ref, ' ja existe essa referencia no arquivo app.js\n')
    else:
        print(ref, ' nao existe, criando os imports e links\n')
        inputfile = open('./src/app.js', 'r').readlines()
        write_file = open('./src/app.js', 'w')
        for line in inputfile:
            write_file.write(line)
            if "import Imoveis from \"./Components/pages/Imoveis\";" in line:
                new_line = "import "+ref+" from \"./Components/pages/imoveis/"+ref+"\";"
                write_file.write(new_line + "\n")
                print('criado import para ' + ref)
            if "                        <Route path=\"imoveis\" element={<Imoveis />}></Route>" in line:
                new_line = "                        <Route path=\"" + \
                    ref+"\" element={<"+ref+" />} />"
                write_file.write(new_line + "\n")
                print('criado link para '+ref)
        write_file.close()

    # closing a file
    file1.close()

    # adding link with ref in /src/components/pages/imoveis.jsx
    # opening a text file
    file1 = open('./src/Components/pages/Imoveis.jsx', "r",encoding='utf-8')

    # read file content
    readfile = file1.read()

    # checking condition for string found or not
    if ref in readfile:
        print(ref, ' ja existe esse link no arquivo de indice\n')
    else:
        print(ref, ' nao existe, criando link no arquivo de indice\n')
        inputfile = open('./src/Components/pages/Imoveis.jsx', 'r',encoding='utf-8').readlines()
        write_file = open('./src/Components/pages/Imoveis.jsx', 'w',encoding='utf-8')
        for line in inputfile:
            write_file.write(line)
            if "                <h1>Casas / Lojas Comerciais</h1>" in line:
                new_line = "                <div style={{display:'flex',gap:'1rem'}}><Link to=\"/"+ref+"\">"+ref+"</Link><p>"+titulo+"</p><p>Tipo: "+finalidade+"</p><p>Valor Locação: "+valor_locacao+"</p><p>Valor Venda: "+valor_venda+"</p></div>"
                write_file.write(new_line + "\n")
                print('Criado link no indice' + ref)
        write_file.close()

def make_qrcode():
    import qrcode
    csv = give_only_ref()
    ref = csv['Referência'].loc[csv.index[0]]

    img = qrcode.make('https://equiplan.com.br/'+ref)
    img.save('./QR CODE DOS IMOVEIS/'+ref+'.png')
    print('criado e salvo como '+ref+'.png\n')


def move_imgs():
    csv = give_only_ref()
    ref = csv['Referência'].loc[csv.index[0]]

    import glob
    import shutil
    import os

    src_folder = r"."
    dst_folder = r"./src/assets/imoveis/"+ref+"/"

    # check if folder exists dest
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
        print('criado nova pasta: '+dst_folder)

    # Search files with .txt extension in source directory
    pattern = "\*.jpg"
    files = glob.glob(src_folder + pattern)

    # move the files with txt extension
    for file in files:
        # extract file name form file path
        file_name = os.path.basename(file)
        shutil.move(file, dst_folder + file_name)
        print('Moved:', file)
    
    if not files:
        print('Nao existe nenhuma foto no diretorio e nada foi feito\n')


menu_options = {
    1: 'csv para pagina',
    2: 'criar qrcode, vai sobreescrever se o arquivo ja existir',
    3: 'mover as imgs(apenas as imgs JPG) para a pasta certo',
    4: 'Sair'
}

if __name__ == '__main__':
    with open('temp','w') as f:
        f.write('')
    csv_to_page()
    make_qrcode()
    move_imgs()
    exit()
