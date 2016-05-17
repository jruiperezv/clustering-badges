from __future__ import division
import models
from google.appengine.ext.db import GqlQuery
from badges import util_badges
import datetime
from viewer_code.profileviewer_models import UserProfile

listaBadgesTematicas = []

for badge in util_badges.badges_tematicas_no_maestro():
    #print badge.exercise_names_required
    listaBadgesTematicas.append(badge.name)
    
usuarios =  GqlQuery("SELECT * FROM UserProfile ORDER BY user_id ASC")

for usuarioID in usuarios:
    
    #print usuarioID
    userData = GqlQuery("SELECT * FROM UserData WHERE user_id = :1", usuarioID).get()

    #print userData.user_id
    topicUserBadges = GqlQuery("SELECT * FROM UserBadge WHERE badge_name IN :1 AND user = :2 ORDER BY date ASC", listaBadgesTematicas, userData.user)
    
    percentageSumForAllTematicBadges = 0
    numberTematicBadges = topicUserBadges.count(1000)
    #print "Tematic Badges %d" % numberTematicBadges

    startDate = datetime.datetime(2013,8,1,0,0,1)
    endDate = None
    for topicUserBadge in topicUserBadges:
        
        #print topicUserBadge

        endDate = topicUserBadge.date
        badge_requisites = ""
        
        for topicBadge in util_badges.badges_tematicas_no_maestro():
            if(topicBadge.name == topicUserBadge.badge_name):
                badge_requisites = topicBadge.exercise_names_required
                #print badge_requisites
        
        #print "Inicio: %s - Fin: %s" % (startDate, endDate)
        
        problemLogBadges = GqlQuery("SELECT * FROM ProblemLog WHERE user = :1 AND time_done >= :2 AND time_done < :3", userData.user, startDate, endDate)
        numberOfProblemLogForTematicBadge = problemLogBadges.count(1000)
        numberOfProblemLogBelongToTematicBadge = 0
		
        for problemLogBadge in problemLogBadges:
            #print problemLogBadge.exercise            
            if any(problemLogBadge.exercise in s for s in badge_requisites):
                numberOfProblemLogBelongToTematicBadge += 1
        
        if(numberOfProblemLogForTematicBadge > 0):
            percentageSumForAllTematicBadges += (numberOfProblemLogBelongToTematicBadge/numberOfProblemLogForTematicBadge)*100

        startDate = topicUserBadge.date
        
        """
        if(numberOfProblemLogForTematicBadge > 0):
            print "Porcentaje parcial %d" % ((numberOfProblemLogBelongToTematicBadge/numberOfProblemLogForTematicBadge)*100)
        """
        
        #print topicBadge.badge_name
        #print topicBadge.date
    if(numberTematicBadges > 0):
        ConcentrationPercentage = percentageSumForAllTematicBadges/numberTematicBadges
    else:
        ConcentrationPercentage = 0
        
    print round(ConcentrationPercentage,2)

