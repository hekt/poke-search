#! /user/bin/env python
# -*- coding: utf-8 -*-

class Translate:
	def __init__(self):
		self.wordsDic = {'nor':'ノーマル', 'fir':'ほのお', 'wat':'みず', 'ele':'でんき', 'gra':'くさ', 'ice':'こおり', 'fig':'かくとう', 'poi':'どく', 'gro':'じめん', 'fly':'ひこう', 'psy':'エスパー', 'bug':'むし', 'roc':'いわ', 'gho':'ゴースト', 'dra':'ドラゴン', 'dar':'あく', 'ste':'はがね'}
	
	def __call__(self, word):
		if self.isAscii(word):
			if word in self.wordsDic:
				return self.wordsDic[word]
			else:
				return word
		else:
			for key in self.wordsDic.keys():
				if word == self.wordsDic[key]:
					return key
			else:
				return word
		
	def isAscii(self, string):
		for i in string:
			if ord(i) > 127:
				return False
		return True
	
	def typeEintoJ(self, word):
		if word in self.wordsDic:
			return self.wordsDic[word]
		return word
		
class Effect:
	def __init__(self):
		nor = {'fig':2, 'gho':0}
		fir = {'fir':0.5, 'wat':2, 'gra':0.5, 'ice':0.5, 'gro':2, 'bug':0.5, 'roc':2, 'ste':0.5}
		wat = {'fir':0.5, 'wat':0.5, 'ele':2, 'gra':2, 'ice':0.5, 'ste':0.5}
		ele = {'ele':0.5, 'gro':2, 'fly':0.5, 'ste':0.5}
		gra = {'fir':2, 'wat':0.5, 'ele':0.5, 'gra':0.5, 'ice':2, 'poi':2, 'gro':0.5, 'fly':2, 'bug':2}
		ice = {'fir':2, 'ice':0.5, 'fig':2, 'roc':2, 'ste':2}
		fig = {'fly':2, 'psy':2, 'bug':0.5, 'roc':0.5, 'dar':0.5}
		poi = {'gra':0.5, 'fig':0.5, 'poi':0.5, 'gro':2, 'psy':2, 'bug':0.5}
		gro = {'wat':2, 'ele':0, 'gra':2, 'ice':2, 'poi':0.5, 'roc':0.5}
		fly = {'ele':2, 'gra':0.5, 'ice':2, 'fig':0.5, 'gro':0, 'bug':0.5, 'roc':2}
		psy = {'fig':0.5, 'psy':0.5, 'bug':2, 'gho':2, 'dar':2}
		bug = {'fir':2, 'gra':0.5, 'fig':0.5, 'gro':0.5, 'fly':2, 'roc':2}
		roc = {'nor':0.5, 'fir':0.5, 'wat':2, 'gra':2, 'fig':2, 'poi':0.5, 'gro':2, 'fly':0.5, 'ste':2}
		gho = {'nor':0, 'fig':0, 'poi':0.5, 'bug':0.5, 'gho':2, 'dar':2}
		dra = {'fir':0.5, 'wat':0.5, 'ele':0.5, 'gra':0.5, 'ice':2, 'dra':2}
		dar = {'fig':2, 'psy':0, 'bug':2, 'gho':0.5, 'dar':0.5}
		ste = {'nor':0.5, 'fir':2, 'gra':0.5, 'ice':0.5, 'fig':2, 'poi':0, 'gro':2, 'fly':0.5, 'psy':0.5, 'bug':0.5, 'roc':0.5, 'gho':0.5, 'dra':0.5, 'dar':0.5, 'ste':0.5}
		
		self.typesEffectList = {'nor':nor, 'fir':fir, 'wat':wat, 'ele':ele, 'gra':gra, 'ice':ice, 'fig':fig, 'poi':poi, 'gro':gro, 'fly':fly, 'psy':psy, 'bug':bug, 'roc':roc, 'gho':gho, 'dra':dra, 'dar':dar, 'ste':ste}
		
		self.effectiveTraitsList = [u'もらいび', u'ちょすい', u'よびみず', u'ちくでん', u'ひらいしん', u'でんきエンジン', u'ふゆう', u'そうしょく', u'たいねつ', u'あついしぼう', u'かんそうはだ']
		
		flashFire = {'fir':0}
		waterAbsorb = {'wat':0}
		stormDrain = {'wat':0}
		voltAbsorb = {'ele':0}
		lightningrod = {'ele':0}
		motorDrive = {'ele':0}
		levitate = {'gro':0}
		sapSipper = {'gra':0}
		heatproof = {'fir':0.5}
		thickFat = {'fir':0.5, 'ice':0.5}
		drySkin = {'fir':1.25, 'wat':0}
		#solidRock = {}
		#filter = {}
		#multiscale = {}
		
		self.traitsEffectList = {u'もらいび':flashFire, u'ちょすい':waterAbsorb, u'よびみず':stormDrain, u'ちくでん':voltAbsorb, u'ひらいしん':lightningrod, u'でんきエンジン':motorDrive, u'ふゆう':levitate, u'そうしょく':sapSipper, u'たいねつ':heatproof, u'あついしぼう':thickFat, u'かんそうはだ':drySkin}
		
	def __call__(self, attackType, targetTypes, targetTrait=''):
		return self.getEffectRate(attackType, targetTypes, targetTrait)
		
	def isConform(self, atType, threshold, dfTypes, compare, trait=''):
		u"""与えられた条件に適合するか調べる
		
		>>> pktools.Effect().isConform('nor', 1, ['ste', 'gra'], 'less')
		True
		>>> pktools.Effect().isConform('nor', 1, ['ste', 'gra'], 'less')
		False
		>>> pktools.Effect().isConform('nor', 0.5, ['ste', 'gra'], 'equal')
		True
		
		"""
		if compare == 'less':
			effectRate = self.getEffectRate(atType, dfTypes, trait)
			if effectRate <= threshold:
				return True
		elif compare == 'more':
			effectRate = self.getEffectRate(atType, dfTypes, trait)
			if effectRate >= threshold:
				return True
		if compare == 'equal':
			effectRate = self.getEffectRate(atType, dfTypes, trait)
			if effectRate == threshold:
				return True
		return False
	
	def isEffectiveTrait(self, q):
		u"""タイプ相性のダメージ計算に影響のある特性かどうかを調べる
		
		>>> pktools.Effect().isEffectiveTrait(u'もらいび')
		True
		>>> pktools.Effect().isEffectiveTrait(u'ものひろい')
		False
		
		"""
		if q in self.effectiveTraitsList:
			return True
		return False
	
	def getEffectRate(self, atType, dfTypes, dfTrait=''):		
		if type(dfTypes) is str or type(dfTypes) is int:
			dfTypes = [dfTypes]
			
		effect = 1
		for i in dfTypes:
			e = self.getTypeEffectsDic(i)
			if atType in e:
				effect *= e[atType]
		if dfTrait:
			e = self.getTraitEffectsDic(dfTrait)
			if atType in e:
				effect *= e[atType]
		return effect
	
	def getTypeEffectsDic(self, type):
		if type in self.typesEffectList:
			return self.typesEffectList[type]
		return {}
	
	def getTraitEffectsDic(self, trait):
		if trait in self.traitsEffectList:
			return self.traitsEffectList[trait]
		return {}
