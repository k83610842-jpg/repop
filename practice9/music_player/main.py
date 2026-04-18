import pygame 
import sys
import pp
def main():
    pygame.init()
    screen=pygame.display.set_mode((600,400))
    pygame.display.set_caption("Music player")
    songs=pp.get_playlist()
    current_track_index=0
    is_playing=False
    my_font=pygame.font.SysFont("Coutier New",18)
    running=True
    while running:
        screen.fill((20,20,20))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    if len(songs)>0:
                        pp.play_song(songs[current_track_index])
                        is_playing=True
                if event.key==pygame.K_s:
                    pygame.mixer.music.stop()
                    is_playing=False
                if event.key==pygame.K_n:
                    if len(songs)>0:
                        current_track_index=(current_track_index+1)%len(songs)
                        pp.play_song(songs[current_track_index])
                        is_playing=True
                if event.key==pygame.K_b:
                    if len(songs)>0:
                        current_track_index=(current_track_index-1)%len(songs)
                        pp.play_song(songs[current_track_index])
                        is_playing=True
                if event.key==pygame.K_q:
                    running=False
        if len(songs)>0:
            name_label=my_font.render("Song " + songs[current_track_index],True,(255,255,255))
            screen.blit(name_label,(50,100))
        status_text="Playing" if is_playing else "Stopped"
        status_label=my_font.render("Status: "+status_text,True,(0,255,255))
        screen.blit(status_label,(50,150))
        controls_label=my_font.render("P:Play S:Stop N:Next B:Back Q:Quit",True,(150,150,150))
        screen.blit(controls_label,(50,300))
        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__=="__main__":
    main()

