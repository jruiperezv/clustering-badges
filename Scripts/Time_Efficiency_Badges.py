from __future__ import division
import models
from google.appengine.ext.db import GqlQuery
from badges import util_badges


listaBadgesEjerciciosNoTematicos = []
listaBadgesEjerciciosTematicos = []
listaBadgesVideos = []

for badge in util_badges.exercise_badges_no_tematic():
    #print badge.exercise_names_required
    listaBadgesEjerciciosNoTematicos.append(badge.name)
    
for badge in util_badges.exercise_badges_only_tematic():
    #print badge.exercise_names_required
    listaBadgesEjerciciosTematicos.append(badge.name)
    
for badge in util_badges.video_badges():
    #print badge.exercise_names_required
    listaBadgesVideos.append(badge.name)
    
queryUserData = models.UserData.all()

usuarios =  GqlQuery("SELECT * FROM UserProfile ORDER BY user_id ASC")

for usuarioID in usuarios:
    
    #print usuarioID
    userData = GqlQuery("SELECT * FROM UserData WHERE user_id = :1", usuarioID).get()

    #print userData.user_id
    
    exerciseUserBadgesNoTematic = GqlQuery("SELECT * FROM UserBadge WHERE badge_name IN :1 AND user = :2", listaBadgesEjerciciosNoTematicos, userData.user)
    exerciseUserBadgesTematic = GqlQuery("SELECT * FROM UserBadge WHERE badge_name IN :1 AND user = :2", listaBadgesEjerciciosTematicos, userData.user)    
    allExerciseUserBadges = list(exerciseUserBadgesNoTematic) + list(exerciseUserBadgesTematic)    
    
    videoUserBadges = GqlQuery("SELECT * FROM UserBadge WHERE badge_name IN :1 AND user = :2", listaBadgesVideos, userData.user)
    
    allUserBadges = GqlQuery("SELECT * FROM UserBadge WHERE user = :1", userData.user)
    
    
    tiempoEnEjercicios = 0
    tiempoEnVideos = 0
    
    videos = models.VideoLog.all().filter('user =', userData.user)
    
    for video in videos:
        tiempoEnVideos += video.seconds_watched/3600
    
    ejercicios = models.ProblemLog.all().filter('user =', userData.user)
    
    for ejercicio in ejercicios:
        tiempoEnEjercicios += ejercicio.time_taken/3600

    tiempoTotalVideosEjercicios = tiempoEnVideos + tiempoEnEjercicios
    
    if(tiempoEnEjercicios != 0):
        badgeEjerciciosEntreTiempo = len(allExerciseUserBadges)/tiempoEnEjercicios
    else:
        badgeEjerciciosEntreTiempo = 0
        
    if(tiempoEnVideos != 0):
        badgeVideosEntreTiempo = videoUserBadges.count(10000)/tiempoEnVideos
    else:
        badgeVideosEntreTiempo = 0
        
    if(tiempoTotalVideosEjercicios != 0):
        badgeTotalEntreTiempo = allUserBadges.count(10000)/tiempoTotalVideosEjercicios
    else:
        badgeTotalEntreTiempo = 0
    
  
    print "%.2f        %.2f        %.2f" % (badgeEjerciciosEntreTiempo,badgeVideosEntreTiempo,badgeTotalEntreTiempo)