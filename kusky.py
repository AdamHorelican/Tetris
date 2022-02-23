import random
import pyglet
from pyglet.window import key
from pyglet import shapes


# todo: 3. otacanie kusku
# todo: 8. ukonecenie hry(game over)



window = pyglet.window.Window(580, 640)
batch = pyglet.graphics.Batch()
zdroj = {
    "I":{"zakladny_tvar":[[360,360,360,360],[420,400,380,360]]},
    "S":{"zakladny_tvar":[[360,380,340,360],[420,420,400,400]]},
    "Z":{"zakladny_tvar":[[340,360,360,380],[420,420,400,400]]},
    "T":{"zakladny_tvar":[[360,360,340,380],[420,400,420,420]]},
    "O":{"zakladny_tvar":[[360,380,360,380],[420,420,400,400]]},
    "L":{"zakladny_tvar":[[360,360,360,380],[420,400,380,380]]},
    "farba":[(255,0,0,),(255, 255, 255),(255, 128, 0),(255, 0, 255),(0, 255, 0),(0, 255, 255),(128, 128, 128)]
}

ulozene_kusky = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0]
]
music_move = pyglet.media.load('line.wav',streaming=False)
music_clear = pyglet.media.load('clear.wav',streaming=False)

level = 1
score_text = 'Score: {}'.format(0)
label = pyglet.text.Label('Tetris',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=600,
                          anchor_x='center', anchor_y='center')

score = pyglet.text.Label(score_text,
                          font_name='Times New Roman',
                          font_size=20,
                          x=100, y=400,
                          anchor_x='center', anchor_y='center')

level_text = 'Level: {}'.format(0)
level = pyglet.text.Label(level_text,
                          font_name='Times New Roman',
                          font_size=20,
                          x=100, y=430,
                          anchor_x='center', anchor_y='center')


class Kusok:
    def __init__(self) -> None:
        super().__init__()
        self.farba = None
        self.zakladny_tvar = []
        self.pohyb = []
        self.velksot = 20
        self.hracia_plocha = []
        self.stare_tvary = []
        self.skore = 0
        self.m = ulozene_kusky
        self.level = 1
        self.rychlost = 0.3

    """"
    tato funckia bude generovat nahodne tvary = [I,S,Z,T,O,L]
    """
    def vygeneruj_nahodny_tvar(self):
        mozne_tvary = ["I","S","Z","T","O","L"]
        # mozne_tvary = ["I"]
        tvar = random.choice(mozne_tvary)
        zaklad = zdroj.get(tvar)
        suradnice = zaklad.get("zakladny_tvar")
        zoznam_farieb = zdroj.get("farba")
        farba = random.choice(zoznam_farieb)
        for i in range(4):
            # print("x = {}, y={}, farba={}".format(suradnice[0][i], suradnice[1][i],farba))
            self.zakladny_tvar.append(shapes.Rectangle(suradnice[0][i],suradnice[1][i],self.velksot,self.velksot,farba, batch=batch))

    """
    aktualny kusok sa posunie s jeho vsetkymi jeho castami vpravo o 20 pixelov vzdy na x-ovej osi
    """
    def kusok_vpravo(self):
        hranica = 480
        pohyb = self.mozem_sa_pohnut_vpravo(hranica,0)
        if pohyb:
            pohyb = self.smiem_sa_pohnut_v_pravo()
        if pohyb:
            tmp = []
            for zt in self.zakladny_tvar:
                #print(zt.position[0])
                tmp.append((shapes.Rectangle(zt.position[0] +20,zt.position[1],self.velksot,self.velksot,zt.color,
                                             batch=batch)))
            self.zakladny_tvar = tmp

    """
    aktualny kusok sa posunie s jeho vsetkymi jeho castami vlavo o 20 pixelov vzdy na x-ovej osi
    """
    def kusok_vlavo(self):
        hranica = 240
        pohyb = self.mozem_sa_pohnut(hranica,0)
        if pohyb:
            pohyb = self.smiem_sa_pohnut_v_lavo()
        if pohyb:
            tmp = []
            for zt in self.zakladny_tvar:
                #print(zt.position[0])
                tmp.append((shapes.Rectangle(zt.position[0] - 20, zt.position[1], self.velksot, self.velksot, zt.color,
                                             batch=batch)))
            self.zakladny_tvar = tmp

    """
    ak sa mozem pohnut tak sa vyska y zmensuje o 20 pixelov, ak je y = 60 gravitacia skonci
    """
    def gravitacia(self):
        hranica = 60
        pohyb = self.mozem_sa_pohnut(hranica,1)
        if pohyb:
            pohyb = k.smiem_sa_pohnut_dole()
        if pohyb:
            tmp = []
            for zt in self.zakladny_tvar:
                #print(zt.position[0])
                tmp.append((shapes.Rectangle(zt.position[0], zt.position[1] - 20, self.velksot, self.velksot, zt.color,
                                             batch=batch)))
            self.zakladny_tvar = tmp

        else:
            """
            vygenerovat novy tvar a ulozit stary          
            """
            for zt in self.zakladny_tvar:
                if zt.position[1] == 400:
                    print("Game over")
                    exit(1)

            self.vloz_kusok_do_matice()
            self.stare_tvary = self.stare_tvary + self.zakladny_tvar
            self.kontroluj_riadok()
            self.zakladny_tvar = []
            self.skontroluj_lietajuce_kocky()

            self.vygeneruj_nahodny_tvar()


    def vloz_kusok_do_matice(self):
        for kocka in self.zakladny_tvar:
            x = kocka.position[0]
            y = kocka.position[1]
            i,j = self.prepocitac_suradnic(x,y)
            self.m[i][j] = 1


    def mozem_sa_pohnut(self, hranica, pozicia):
        for kocka in self.zakladny_tvar:
            if kocka.position[pozicia] <= hranica:
                return False
        return True


    def mozem_sa_pohnut_vpravo(self, hranica, pozicia):
        for kocka in self.zakladny_tvar:
            if kocka.position[pozicia] >= hranica:
                return False
        return True


    def generovanie_hranic(self):
        farba = (255,0,0)
        self.hracia_plocha.append(shapes.Rectangle(240,60,260,1,farba, batch=batch))
        self.hracia_plocha.append(shapes.Rectangle(240,60,1,380,farba, batch=batch))
        self.hracia_plocha.append(shapes.Rectangle(500,60,1,380,farba, batch=batch))
        self.hracia_plocha.append(shapes.Rectangle(240,440,260,1,farba, batch=batch))


    def prepocitac_suradnic(self,x,y):
        mapovac_x = {240:0,260:1,280:2,300:3,320:4,340:5,360:6,380:7,400:8,420:9,440:10,460:11,
                     480:12}
        j = mapovac_x.get(x)
        mapovac_y = {60:18,80:17,100:16,120:15,140:14,160:13,180:12,200:11,220:10,240:9,260:8,
                     280:7,300:6,320:5,340:4,360:3,380:2,400:1,420:0}
        i = mapovac_y.get(y)
        return i, j


    def smiem_sa_pohnut_dole(self):
        pohyb = True
        for kocka in self.zakladny_tvar:
            x = kocka.position[0]
            y = kocka.position[1]
            i,j = self.prepocitac_suradnic(x,y)
            nasledujuci_stav = self.m[i+1][j]
            aktualny_stav =  self.m[i][j]
            # print("x = {}, y = {} # j = {},i = {}, aktualny_stav = {}, nasledujuci_stav = {}".format(x,y,j,i,aktualny_stav,nasledujuci_stav))
            #if ulozene_kusky[j][i+1]
            if nasledujuci_stav == 1:
                pohyb = False
        return pohyb

    def smiem_sa_pohnut_v_lavo(self):
        pohyb = True
        for kocka in self.zakladny_tvar:
            x = kocka.position[0]
            y = kocka.position[1]
            i,j = self.prepocitac_suradnic(x,y)
            nasledujuci_stav = self.m[i][j-1]
            aktualny_stav =  self.m[i][j]
            # print("x = {}, y = {} # j = {},i = {}, aktualny_stav = {}, nasledujuci_stav = {}".format(x,y,j,i,aktualny_stav,nasledujuci_stav))
            #if ulozene_kusky[j][i+1]
            if nasledujuci_stav == 1:
                pohyb = False
        return pohyb

    def smiem_sa_pohnut_v_pravo(self):
        pohyb = True
        for kocka in self.zakladny_tvar:
            x = kocka.position[0]
            y = kocka.position[1]
            i,j = self.prepocitac_suradnic(x,y)
            nasledujuci_stav = self.m[i][j+1]
            aktualny_stav =  self.m[i][j]
            # print("x = {}, y = {} # j = {},i = {}, aktualny_stav = {}, nasledujuci_stav = {}".format(x,y,j,i,aktualny_stav,nasledujuci_stav))
            #if ulozene_kusky[j][i+1]
            if nasledujuci_stav == 1:
                pohyb = False
        return pohyb

    def kontroluj_riadok(self):
        t = 0
        plne_riadky = []
        for k in self.m:
            skore_v_riadku = sum(k)
            #print("Kontrolujem riadok = {}, riadok = {}, sucet = {}".format(t,k,skore_v_riadku))
            if skore_v_riadku == 13:
                plne_riadky.append(t)
            t = t + 1
        pocet_plnych_riadkov = len(plne_riadky)

        if pocet_plnych_riadkov > 0:
            plne_riadky.sort(reverse=True)
            for riadok in plne_riadky:
                e = 0
                for e in range(13):
                    self.m[riadok][e] = 0
                    e = e + 1

            self.skore = self.skore + 100 * pocet_plnych_riadkov
            if self.skore % 100 ==0:
                self.level = self.level + 1
                self.rychlost = self.rychlost + 0.1
            score.text = 'Score: {}'.format(self.skore)
            level.text = 'Level: {}'.format(self.level)
            print("Speed: {}".format(self.rychlost))

            u = 0
            mapovac_i = {18: 60, 17: 80, 16: 100, 15: 120, 14: 140, 13: 160, 12: 180, 11: 200, 10: 220, 9: 240,
                         8: 260, 7: 280, 6: 300, 5: 320, 4: 340, 3: 360, 2: 380, 1: 400, 0: 420}

            tmp_tvary = self.stare_tvary
            for r in plne_riadky:
                y = mapovac_i.get(r)
                if u > 0:
                    y = y - 20 * u
                docasne_kocky = []
                for kocka in tmp_tvary:
                    if kocka.position[1] != y:

                        if kocka.position[1]>y:
                            a = kocka.position[0]
                            b = kocka.position[1] - 20
                            farba = kocka.color
                            docasne_kocky.append(shapes.Rectangle(a, b, 20, 20, farba, batch=batch))
                        else:
                            docasne_kocky.append(kocka)
                tmp_tvary = docasne_kocky

                u = u + 1
            self.stare_tvary = []
            self.stare_tvary = tmp_tvary
            self.prehraj_pohyb()

    def skontroluj_lietajuce_kocky(self):
        z = []
        for t in range(19):
            r = []
            for s in range(13):
                r.append(0)
            z.append(r)
        self.m = z
        for kocka in self.stare_tvary:
            x = kocka.position[0]
            y = kocka.position[1]
            i, j = self.prepocitac_suradnic(x,y)
            self.m[i][j] = 1

    def prehraj_pohyb(self):
        music_clear.play()

    def prehraj_zburanie_riadku(self):
        music_move.play()

k = Kusok()


@window.event
def on_key_press(symbol, modifiers):
    # global board
    if symbol == key.LEFT:
        k.kusok_vlavo()
        k.prehraj_zburanie_riadku()

    elif symbol == key.RIGHT:
        k.kusok_vpravo()
        k.prehraj_zburanie_riadku()

    elif symbol == key.DOWN:
        k.gravitacia()
        k.prehraj_zburanie_riadku()

@window.event
def on_draw():
    window.clear()
    label.draw()
    batch.draw()
    score.draw()
    level.draw()



def pregenerovanie(t):
    k.gravitacia()



if __name__ == '__main__':
    k.vygeneruj_nahodny_tvar()
    k.generovanie_hranic()
    #k.kontroluj_riadok()
pyglet.clock.schedule_interval(pregenerovanie, k.rychlost)
pyglet.app.run()

