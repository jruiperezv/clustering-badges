from __future__ import division
from models import Video
from models import Exercise
from viewer_code.profileviewer_models import UserProfile
import models


from google.appengine.ext.db import GqlQuery
from badges.models_badges import UserBadge
from badges import util_badges

listaBadges = []

for badge in util_badges.badges_tematicas_no_maestro():
    #print badge.exercise_names_required
    listaBadges.append(badge.name)


"""
listaBadgeOrdenadas = sorted(util_badges.badges_tematicas_no_maestro(), key=lambda x: len(x.exercise_names_required), reverse=False)
for badgeOrdenada in listaBadgeOrdenadas:
    print len(badgeOrdenada.exercise_names_required)
    print badgeOrdenada.description
"""

usuarios =  GqlQuery("SELECT * FROM UserProfile ORDER BY user_id ASC")

for usuarioID in usuarios:
    
    #print usuarioID.user_id

    userData = GqlQuery("SELECT * FROM UserData WHERE user_id = :1", usuarioID.user_id).get()

    
    numberOfTematicBadges = 0
    for userBadge in userData.badges:
        if(listaBadges.count(userBadge) >= 1):
            numberOfTematicBadges += 1
    
    #print "Proficient exercises %s" % str(len(userData.all_proficient_exercises))
    
    max_badges = util_badges.max_badges().get(str(len(userData.all_proficient_exercises)))
    #print "Badges: %d" % numberOfTematicBadges
    #print "Max Badges: %d" % max_badges
    
    if(max_badges == 0):
        percentageMinMaxBadges = 0
    else:
        percentageMinMaxBadges = (numberOfTematicBadges/max_badges)*100
    print round(percentageMinMaxBadges,2)
    #print ""
    