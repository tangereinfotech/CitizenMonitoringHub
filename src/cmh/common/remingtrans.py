# encoding: utf-8
# Copyright 2011, Tangere Infotech Pvt Ltd [http://tangere.in]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class RemingTrans ():
    def __init__ (self, *args, **kwargs):
        self.KM = {}
        self.KM["`"] = u"\u0943"         # prev, handled
        self.KM["1"] = u"1"
        self.KM["2"] = u"2"
        self.KM["3"] = u"3"
        self.KM["4"] = u"4"
        self.KM["5"] = u"5"
        self.KM["6"] = u"6"
        self.KM["7"] = u"7"
        self.KM["8"] = u"8"
        self.KM["9"] = u"9"
        self.KM["0"] = u"0"
        self.KM["-"] = u"."
        self.KM["="] = u"\u0924\u094D\u0930"

        self.KM["~"] = u"\u094D"         # better char needed, seems to be an explicit non-removable halant
        self.KM["!"] = u"!"
        self.KM["@"] = u"/"
        self.KM["#"] = u"\u0930\u0941"
        self.KM["$"] = u"+"
        self.KM["%"] = u"\u0903"         # prev
        self.KM["^"] = u"\u0027"
        self.KM["&"] = u"\u2014"
        self.KM["*"] = u"\u0027"
        self.KM["("] = u""
        self.KM[")"] = u"\u0926\u094D\u0927"
        self.KM["_"] = u"\u090B"
        self.KM["+"] = u"\u093C"         # prev

        self.KM["q"] = u"\u0941"           # prev
        self.KM["w"] = u"\u0942"           # prev
        self.KM["e"] = u"\u092E"
        self.KM["r"] = u"\u0924"
        self.KM["t"] = u"\u091C"
        self.KM["y"] = u"\u0932"
        self.KM["u"] = u"\u0928"
        self.KM["i"] = u"\u092A"
        self.KM["o"] = u"\u0935"
        self.KM["p"] = u"\u091A"
        self.KM["["] = u"\u0916\u094D"
        self.KM["]"] = u"\u002C"
        self.KM["\\"] = u"?"

        self.KM["Q"] = u"\u092B"
        self.KM["W"] = u"\u0945"        # prev
        self.KM["E"] = u"\u092E\u094D"
        self.KM["R"] = u"\u0924\u094D"
        self.KM["T"] = u"\u091C\u094D"
        self.KM["Y"] = u"\u0932\u094D"
        self.KM["U"] = u"\u0928\u094D"
        self.KM["I"] = u"\u092A\u094D"
        self.KM["O"] = u"\u0935\u094D"
        self.KM["P"] = u"\u091A\u094D"
        self.KM["{"] = u"\u0915\u094D\u0937\u094D"
        self.KM["}"] = u"\u0926\u094D\u0935"
        self.KM["|"] = u"\u0926\u094D\u092F"

        self.KM["a"] = u"\u0902"
        self.KM["s"] = u"\u0947"
        self.KM["d"] = u"\u0915"
        self.KM["f"] = u"\u200B\u093F"  # special treatment - chhoti ee, reverse characters
        self.KM["g"] = u"\u0939"
        self.KM["h"] = u"\u0940"
        self.KM["j"] = u"\u0930"
        self.KM["k"] = u"\u093E"        # special treatment - "a"kar or "aa"kar, remove halant if present
        self.KM["l"] = u"\u0938"
        self.KM[";"]  = u"\u092F"
        self.KM["'"] = u"\u0936\u094D"

        self.KM["A"] = u"\u0964"
        self.KM["S"] = u"\u0948"
        self.KM["D"] = u"\u0915\u094D"
        self.KM["F"] = u"\u0925\u094D"
        self.KM["G"] = u"\u0933"
        self.KM["H"] = u"\u092D\u094D"
        self.KM["J"] = u"\u0936\u094D\u0930"
        self.KM["K"] = u"\u091C\u094D\u091E"
        self.KM["L"] = u"\u0938\u094D"
        self.KM[":"] = u"\u0930\u0942"
        self.KM["\""] = u"\u0937\u094D"

        self.KM["z"] = u"\u094D\u0930"
        self.KM["x"] = u"\u0917"
        self.KM["c"] = u"\u092C"
        self.KM["v"] = u"\u0905"
        self.KM["b"] = u"\u0907"
        self.KM["n"] = u"\u0926"
        self.KM["m"] = u"\u0909"
        self.KM[","] = u"\u090F"
        self.KM["."] = u"\u0923\u094D"
        self.KM["/"] = u"\u0927\u094D"

        self.KM["Z"] = u"\u0930\u094D"
        self.KM["X"] = u"\u0917\u094D"
        self.KM["C"] = u"\u092C\u094D"
        self.KM["V"] = u"\u091F"
        self.KM["B"] = u"\u0920"
        self.KM["N"] = u"\u091B"
        self.KM["M"] = u"\u0921"
        self.KM["<"] = u"\u0922"
        self.KM[">"] = u"\u091D"
        self.KM["?"] = u"\u0918\u094D"


        self.halant = u"\u094D"
        self.zwsp   = u"\u200b"
        self.akar   = self.KM ["k"]
        self.ikar   = u"\u093F"
        self.rkar   = self.KM ["z"]
        self.aukar  = self.KM ["W"]
        self.ekar   = self.KM ["s"]
        self.aekar  = self.KM ["S"]
        self.raif   = self.KM ["Z"]
        self.nukta  = self.KM ["+"]
        self.okar   = u"\u094B"
        self.aokar  = u"\u094C"
        self.chhoti_ee = u"\u0907"
        self.badi_ee = u"\u0908"
        self.all_matras = [self.KM ["k"], self.KM ["h"], self.KM ["q"], self.KM ["w"],
                           self.KM ["s"], self.KM ["S"], self.KM ["a"], self.halant,
                           self.KM ["f"], self.KM ["h"], self.okar, self.aokar, self.aukar, self.ikar, self.raif,
                           self.rkar, self.nukta]

    def handle_raif (self, orgstr, mappedKey):
        lrets = orgstr + mappedKey

        for i in range ((len (orgstr) - 1), -1, -1):
            if (orgstr [i] in self.all_matras):
                continue
            else:
                pre_orgstring = orgstr [ : i]
                pst_orgstring = orgstr [i : ]
                lrets = pre_orgstring + mappedKey + pst_orgstring
                break
        return lrets


    def handle_nukta (self, orgstr, mappedKey):
        lrets = orgstr + mappedKey

        for i in range ((len (orgstr) - 1), -1, -1):
            if (orgstr [i] in self.all_matras):
                continue
            else:
                pre_orgstring = orgstr [ : i + 1]
                pst_orgstring = orgstr [i + 1 : ]
                lrets = pre_orgstring + mappedKey + pst_orgstring
                break
        return lrets


    def itrans (self, oldStr, curChar):
        pchr = ""
        ppch = ""
        pstr = ""
        ppst = ""

        if len (oldStr) != 0:
            pchr = oldStr [-1 : ]
            pstr = oldStr [ : -1]

            if len (oldStr) != 1:
                ppch = oldStr [-2 : ]
                ppst = oldStr [ : -2]

        if curChar in self.KM.keys ():
            mapped = self.KM [curChar]

            if pchr == self.ikar:
                if ppch == self.zwsp:
                    if mapped == self.raif:
                        rets = self.handle_raif (ppst, self.raif) + self.ikar
                    elif mapped == self.nukta:
                        rets = self.handle_nukta (ppst, self.nukta) + self.ikar
                    elif mapped == self.rkar:
                        rets = pstr + self.rkar + self.ikar
                    else:
                        if mapped [-1 : ] == self.halant:
                            rets = ppst + mapped [: -1] + self.ikar + self.halant
                        else:
                            rets = ppst + mapped + self.ikar
                else:
                    if mapped == self.raif:
                        rets = self.handle_raif (pstr, self.raif) + self.ikar
                    elif mapped == self.nukta:
                        rets = self.handle_nukta (pstr, self.nukta) + self.ikar
                    elif mapped == self.rkar:
                        rets = pstr + self.rkar + self.ikar
                    else:
                        rets = oldStr + mapped
            else:
                if mapped == self.rkar:
                    if pchr == self.halant:
                        rets = pstr + self.rkar + self.halant
                    else:
                        rets = oldStr + self.rkar
                elif mapped == self.nukta:
                    rets = self.handle_nukta (oldStr, self.nukta)
                elif mapped == self.raif:
                    if pchr == self.chhoti_ee:
                        rets = pstr + self.badi_ee
                    else:
                        rets = self.handle_raif (oldStr, self.raif)
                elif mapped == self.akar:
                    if len (oldStr) == 0:
                        rets = self.akar
                    else:
                        if pchr == self.halant:
                            rets = pstr
                        elif pchr == self.KM ["v"]:
                            rets = pstr + u"\u0906"
                        else:
                            rets = oldStr + self.akar
                elif mapped == self.aukar:
                    if pchr == self.akar:
                        rets = pstr + u"\u0949"
                    else:
                        rets = oldStr + mapped
                elif mapped == self.ekar:
                    if pchr == self.akar:
                        rets = pstr + self.okar
                    elif pchr == u"\u0906":
                        rets = pstr + u"\u0913"
                    elif pchr == self.KM [","]:
                        rets = pstr + u"\u0910"
                    else:
                        rets = oldStr + mapped
                elif mapped == self.aekar:
                    if pchr == self.akar:
                        rets = pstr + self.aokar
                    elif pchr == u"\u0906":
                        rets = pstr + u"\u0914"
                    else:
                        rets = oldStr + mapped
                else:
                    if pchr == self.halant and ppch == self.ikar:
                        if mapped.substring [-1 : ] == self.halant:
                            rets = ppst + self.halant + mapped [ : -1] + self.ikar + self.halant
                        else:
                            rets = ppst + self.halant + mapped + self.ikar
                    else:
                        rets = oldStr + mapped
        else:
            rets = oldStr + curChar

        return rets

def translate (sentence):
    rt = RemingTrans ()
    ts = ""
    for c in sentence:
        ts = rt.itrans (ts, c)
    return ts


