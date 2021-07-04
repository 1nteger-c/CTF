from Crypto.Util.number import *

N = 123850820426090063939750639461336535800888872303996740868393788108622197265459429269747101462736954752274429639803614452794471290719054376275608856319222801843407104278834963103014930163521479153822223511859077469170499658852892275556238914610902748238728617276564375256445353397161395711740355127024574224311
c = 56546264931253064991800011273062933350432906376123256400827688151463707024780705798157442404868856565703869323810835490194009709876675990770476983384812994742572992276677277260443081273365933217994869622952757076883760367020628026475789906867095354686131932884540071471310629032433408073596634685260647480557
prime = 6880599843336662467879109387236213815987292188507187559989074121615354243311606616327703377828006351833629583392546362975490427453804091142854644316412663
seed = 6115683512551493681429013672578437250992709174507633110965073551143324876511315798363722262299405597781297506013981949713431316382568201987118489728973776

leak = [365273572660559,228957749427794,1023871873444793,47252622313084,621483163501141,1613904529954105,670371640095186,746154892348423,273487816490195,151531815782072,1662852876327887,1698199163478340,1075397252623564,1505608634604579,349759022277267,1134428317370092,1914468910812945,1449958424107745,1708263912457545,1608955265676391,962961718578747,492775505618570,1449265435907005,1077616772328631,420940837638395,769389932722088,549881519479757,1676426597279872,1573991110103234,1400714164789778,581968837775620,1376374167375553,1841940053587716,420575338863847,299279483936789,1186210612325224,558893222798419,1215393260436589,1621782119801357,1320723047102254,1910717961955659,422371988218178,1513263394020288,956317417537022,1567996439899881,2193173496691391,566736180966973,81481592808825,868887510227897,897432919933712,1419950508122052,2253104843374582,1314588757176622,1349424195128398,659859552921929,1240565365943525,1693900629547647,1525267164169311,1386373255161464,1536113899311190,56234973351024,1925918815506579,287836215793395,389246591225136,1883177625103946,246236676888424,1944447510201202,608299716617507,2243764093782209,1077408515947411,1138642240666237,1751463533818637,1558555079410531,252098100710701,2239430963100067,2135594922481591,1688483945377282,1549666800062663,1464365625092491,185536557129512,1004362472376337,1948808921789811,2031903620443744,2066731879678723,578914720736828,1363465325184714,1433811139961805,1742483803193365,572175546886313,340979809399667,2171912600026334,1001051821134338,920690743143218,477941886516671,1774215443756664,1982565638845698,166099725703156,2039256848643079,1454907268385438,1603061507691847,2113704084012013,2062092461008443,1614285283894297,759891517833802,1933991890191651,1177925124477624,1686016253481693,2209855994715577,1584350556327567,593731528964815,2083066020813294,2067296679145133,689829581647088,479369674173931,883198559498913,1884907467679494,1014311704919724,754288839180058,1877376912607021,1823444794770617,869728455696930,1864749572741264,1576512935738044,1920494272459775,475282365166640,1547909564519771,1072200754479187,1447950537071799,948325829047773,1454652268959382,413950997951054,179876655529469,316322757161915,1213922549580749,766210166059710,2027301859734191,1133004743606733,2151399978580323,1491074155967000,374252276953386,413251654097948,674423904166975,1923710400363006,939078022522962,551433636957783,920487928633848,2229216155425176,1514460702803065,101282672877916,1231536851493911,817066453849768,1821037449806754,1785440539579619,567403253985889,2026106354461017,148498723126041,2270407174853085,1641168597532922,2289358538467132,139429775743343,676845953850845,2174753880306469,116625659234205,1459734450825718,975035393647684,527839506174836,409604259076605,405810742317469,2230572864819011,2111976384057693,1010755791098506,2249903249031774,1295962383729844,611323710580353,1599339020692593,480416184280072,1617286128325568,928274387980042,506796759542092,1197623032961027,372872018444,1788636647737738,1787946862093433,491126743054673,1289460442319696,1750036145448962,2287699795049243,2068193669828051,2133121457298840,1186681523752311,535668657124933,2157018791958130,63918446189908,1114159378095436,709574049560819,1320201392088036,1691566118724085,1615369417111975,960416212157945,961170133381721]

## round 1 -> recover p's chunk by Hidden Number Problem (HNP)
out = []
for off in range(4):
    s = seed
    use = leak[off::4]
    n = len(use)
    for i in range(off):
        s = pow(s,2,prime)
    M = Matrix(ZZ,n+2,n+2)
    for i in range(n):
        M[0,i] = s
        s = pow(s,16,prime)
        M[i+1,i] = prime
        M[n+1,i] = use[i] << 460
    M[0,n] = 1
    M[1+n,n+1] = 2**512
    get = M.LLL()[-1]
    out.append(get[-2] * -1)

print('recover yeah !! ',out)

## round 2 -> recover left bits by Multivariate Coppersmith Attack
load("multivariate_coppersmith.sage")
size = 146
known = 0
unknown = []
for i in range(1,4):
    tmp = (146*i-35,35)
    unknown.append(tmp)
for i in range(4):
    known += out[i] << (size * i)
unknown = [(111, 35), (257, 35), (403, 35)]
known = 10571149853133522431404264421866395513173821523643894835630672288391956736188404880335540994971314013670900609488503094055472955457681524945615744534010765
ans = solve(N, unknown, known,beta=0.5, m=6, t=1)
print('recover yeah !!',ans)
p = 0
for i in range(len(out)):
    p += out[i] << (size * i)

for i in range(len(ans)):
    p += ans[i] << (size * (i+1) - 35)

assert N % p == 0
q = N // p
phi = (p-1) * (q-1)
d = inverse(0x10001,phi)
print(long_to_bytes(pow(c,d,N)))