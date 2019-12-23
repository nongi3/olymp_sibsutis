from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import apiclient.discovery

all_handles = [
"nongi",
"UWPLP",
"kcherdakov",
"Qalmee",
"genybr",
"Mazx1998",
"stMark",
"Thundbird",
"bedsus",
"Allen_Mett",
"Shadow-of-Dreams",
"Levcor",
"andrew_raiden",
"niloniol",
"Mary12",
"Minddarkness",
"PowerOfBalls",
"Alecks",
"Tornem",
"ikrisi",
"RushBush",
"fkz_12",
"Arishenk",
"Flanterz",
"Fonriter98",
"ruban",
"jeanstefanovich",
"Brandon_Roadgears_",
"Soul_Catcher",
"shise",
"Izeytee",
"wartemw",
"deluck",
"gedenteen",
"Marks53",
"Dream_Tea",
"Kagary",
"F14rk",
"JustBoss",
"Animeshka",
"Lampcomm",
"Nottey",
"alexger1999",
"Tod-cun",
"osipovcf",
"MikeAirone",
"Karina8941",
"Aleksey-Kn",
"Makisto",
"Asakujaku",
"Hostel_B",
"fredboy",
"aldinger_a",
"Restov",
"BarebuhPuh",
"virride",
"Hazzi",
"fancyFox",
"Sheshesi",
"Gadyka",
"Grawyn",
"Baburr",
"tryblyat7",
"MangriMen",
"_HiFive",
"QWOP1234",
"Daniil_hrpo",
"isugihere",
"sweetechka",
"El_Duderino",
"QualDiv2",]

spreadsheet_id = '1gJYZf7wQE0ReIgR8idpZnqqgSPKQmlkQtnaO3XwGcJI'
os_goods_sh_id = '1fK6aylovMO_8fCRDG2AWE_4gZDjJHw5URLwU-fm0Nkc'

token = "0d58da257245ff2850c27b089689277341398df66c38a7ff052417f0f89ccef5c6e902a30e934c67f6bc0"

accecc_token = '8a520237d2aba831b8258f4be3d5a481396495297fd7627c41754a80098936ed3bb698584089e6016708e'

CREDENTIALS_FILE = 'creds.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
