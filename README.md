# Geração do XML para histórico e grade do aluno.
Version: 2.0
Gato de Schrodinger

<br>

## Info:
#### Libs:
* selenium    → Automatiza o navegador
* bs4         → Html
* html5lib    → 'parser' necessário para o bs4
* textract    → PDF 
```bash
 sudo apt install swig          # dependencia do textract (instalacao)
 sudo apt install libpulse-dev  # dependencia do textract (pulseaudio)
```
#### Instalação:
```bash
 sudo apt install swig libpulse-dev 
 sudo pip install bs4 html5lib textract
 ```
#### Remoção:
```bash
sudo apt autoremove swig libpulse-dev 
sudo pip uninstall bs4 html5lib textract
```
#### Configurações:
* Navegador Chrome → versão 74.0.3729.108 (Official Build) (64-bit)
* Chrome webdriver → versão 74.0.3729.6

<br>

## Pastas:
* **packages:** Programas que foram desenvolvidos para auxiliar na main, i.e., módulos
* **webdriver:** arquivo necessário para a automatização do Google Chrome (chromedriver)
* **xml_files:** respostas, ou seja, os arquivos gerados em xml, tanto para a grade, quanto para o histórico.
* **doc:** documentação em doxygen do código e arquivos auxiliares.
* **.temp_files:** usada para guardar o arquivo do histórico.
* **logs:** pasta que contém os arquivos de log da classe `SScraping`
> Caso não tenha todas essas pastas (geralmente vazias):
> ```bash
> mkdir xml_files .temp_files logs
> ```

<br>

## Arquivos:

#### **/packages**
**SScraping**
1. *BasicXml*, classe para gerar o XML
2. *SScraping*, classe para fazer a raspagem

**\_\_init\_\_.py**, configura para que entenda a pasta como um módulo do python

#### **/webdriver**
    *chromedriver*, ferramenta necessária para rodar o teste 'automatizado'
