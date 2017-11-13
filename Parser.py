from bs4 import BeautifulSoup
import requests, zipfile, psycopg2, time
url = 'http://data.gov.ua/sites/default/files/media/document/911/05.09.2016/uo.zip'
zip_file = url.split('/')[-1]

try:
    conn = psycopg2.connect("dbname='uo_db2' user='alex_korentsvit' host='localhost' password='qwerty'")
except:
    print ("I am unable to connect to the database")
else:
    print('successfully connected to the database')
    cur = conn.cursor()






def download(url, zip_file):
    try:
        req = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Seems like problems with Internet connection..')
    else:
        with open(zip_file,"wb") as uo:
            uo.write(req.content)
        del req
        return True
    return False


def unarchiv(zip_file):
    try:
        archiv = zipfile.ZipFile(zip_file, 'r')
    except FileNotFoundError:
        err_msg = "Can't find the zip file: {}".format(zip_file)
        print(err_msg)
    else:
        global File_name
        File_name = archiv.namelist()[0]
        archiv.extract(File_name)
        return True
    return False



def CreateDb(cur):
    try:
        cur.execute("CREATE TABLE UO_TABLE (id serial PRIMARY KEY, Name text, Short_name text, EDRPOU_code text, Location text, Name_Manager text, Type_of_activity text, State text);")
    except:
        print ("Can't create the table")
    else:
        return True
    return False


def Filling_table(File_name, conn, cur):
    keys = ['Найменування', 'Скорочена_назва', 'Код_ЄДРПОУ', 'Місцезнаходження', 'ПІБ_керівника', 'Основний_вид_діяльності', 'Стан']
    doc = ''
    info = {}
    with open(File_name) as File:
        my_lines = File.readlines()
        
    for line in my_lines:
        doc = line
        if doc == '</ROW>\n':
           print('---------------------------------------')
           print(info)
           print('---------------------------------------')
           cur.execute("INSERT INTO UO_TABLE (Name, Short_name, EDRPOU_code, Location, Name_Manager, Type_of_activity, State) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (str(info['Найменування']), str(info['Скорочена_назва']), str(info['Код_ЄДРПОУ']), str(info['Місцезнаходження']), str(info['ПІБ_керівника']), str(info['Основний_вид_діяльності']), str(info['Стан'])))
           info = {}
        else:
            soup = BeautifulSoup(''.join(doc), features="xml")
            try:
                soup.contents[0].name
            except:
                print('There is no content on this line')
            else:
                if soup.contents[0].name in keys:
                    info[soup.contents[0].name] = soup.contents[0].string
        
    conn.commit()
    cur.close()
    conn.close()
    File.close()
    return True




def Master():
    start = time.time()
    if download(url, zip_file) == True:
        print('the archive is successfully downloaded')
    if unarchiv(zip_file) == True:
        print('the archive is successfully unpacked')
    if CreateDb(cur) == True:
        print('successfully created a table')
    if Filling_table(File_name, conn, cur) == True:
        print('table successfully filled')
    Time = time.time() - start
    print("Lead Time: " + str(Time))
    
    
Master()

