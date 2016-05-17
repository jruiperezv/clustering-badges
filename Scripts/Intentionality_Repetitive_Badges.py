from __future__ import division
import models
from google.appengine.ext.db import GqlQuery
from badges import util_badges
from viewer_code.profileviewer_models import UserProfile

listaBadgesRepetidas = []

for badge in util_badges.repetitive_badges_exercises():
    #print badge.exercise_names_required
    listaBadgesRepetidas.append(badge.name)

# Todos los usuarios del curso
usuarios =  GqlQuery("SELECT * FROM UserProfile ORDER BY user_id ASC")


for usuarioID in usuarios:
    
    #print usuarioID
    userData = GqlQuery("SELECT * FROM UserData WHERE user_id = :1", usuarioID).get()

    #print userData.user_id
    repetitiveUserBadges = GqlQuery("SELECT * FROM UserBadge WHERE badge_name IN :1 AND user = :2", listaBadgesRepetidas, userData.user)
    
    repetitiveBadgesAfterProficiency = 0
    for repetitiveBadge in repetitiveUserBadges:

        userExercise = GqlQuery("SELECT * FROM UserExercise WHERE exercise_model = :1 AND user = :2", repetitiveBadge.target_context, userData.user).get()
        #print "Fecha prof %s" % userExercise.proficient_date
        #print "Fecha badg %s" % repetitiveBadge.date
        
        if(userExercise.proficient_date != None):
            if(repetitiveBadge.date > userExercise.proficient_date):
                repetitiveBadgesAfterProficiency += 1
                #print "Es Mayor"
                
                
    if(repetitiveUserBadges.count(10000) > 0):
        percentageRepetitiveAfterProf = (repetitiveBadgesAfterProficiency/repetitiveUserBadges.count(10000))*100
    else:
        percentageRepetitiveAfterProf = 0
        
    print round(percentageRepetitiveAfterProf,2)
        
