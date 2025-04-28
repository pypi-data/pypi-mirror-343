
from moviepy import  VideoFileClip, AudioFileClip, concatenate_videoclips, afx, CompositeAudioClip, vfx
import os
import random

def interfaceUtils():

    # Chamada config troca para teste direto

    # import utils
    # return utils.config_paths()

    return {
        "path_root": "C:\\Users\\will_\\OneDrive\\Documentos\\GitHub\\Contos-Magicos\\",
        "path_base_comfy": "W:\\Youtube\\confyui\\models\\",
        "historic_history": "w:\\Youtube\\ContosMagicos\\controle.json",
        "path_video_out": "W:\\Youtube\\confyui\\comfyui_out\\",
        "path_video": "W:\\Youtube\\confyui\\comfyui_out\\",
        "path_history": "W:\\Youtube\\ContosMagicos\\History\\",
        "path_audio" : "W:\\Youtube\\ContosMagicos\\Narration\\audios\\",
        "path_FX" : "W:\\Youtube\\FX\\",
        "path_model": "W:\\Youtube\\ContosMagicos\\Narration\\model\\",
        "path_ref": "W:\\Youtube\\ContosMagicos\\Narration\\vozes\\",
        "path_youtube_video": "W:\\Youtube\\ContosMagicos\\youtube_video\\"
    }




def findVideos(id_selec, config):
    lista_videos = {}
    print("Vídeos Selecionados:------")
    for i in sorted(os.listdir(config["path_video"])):
        split = i.split("_")
        id = split[0]+"_"+split[1]

        if str(id_selec) == str(id):
            num = split[2]
            temp_video =VideoFileClip(config["path_video"]+i) 
            lista_videos[str(num)] = temp_video.with_effects([vfx.MultiplySpeed(0.5)])
    lista_videos = dict(sorted(lista_videos.items(), key=lambda x: int(x[0])))
    return lista_videos

            


def findAudios(id_selec, config):
    
    lista_audio = {}
    dir_video = os.path.join(config["path_audio"], str(id_selec))
    pasta = sorted(list(os.listdir(dir_video)))
    print("Audios Selecionados:------")
    for lang in ["pt","ar", "en", "es", "fr", "de", "it", "pl", "tr", "ru", "nl", "cs",  "zh-cn"]:
        aux = {}
        for i in pasta:
            split = i.split("_")
            id = split[0]+"_"+split[1]
            if str(id_selec) == str(id) and split[4] == lang:
                num = split[3].replace(".wav","")
                aux[str(num)]=AudioFileClip(config["path_audio"]+"/"+str(id)+"/"+i)
        lista_audio[lang] = dict(sorted(aux.items(), key=lambda x: int(x[0])))

    return lista_audio
            

def findFX(config):
    print("Buscando FX-------")
    fx_list = os.listdir(config["path_FX"])
    fx_selec = random.randint(0, len(fx_list)-1)
    return config["path_FX"]+fx_list[fx_selec]


def run(id):
    print("Iniciando Edição")
    config = interfaceUtils()
    set_audios = findAudios(id, config)
    set_videos = findVideos(id, config)
    set_fx     = findFX(config)

    

    print("Mixando audio......")

    fx = AudioFileClip(set_fx)
    fx = fx.with_effects([afx.MultiplyVolume(0.2)])

    
    
    for lang in ["ar", "en", "es", "fr", "de", "it", "pl", "tr", "ru", "nl", "cs",  "zh-cn", "pt"]:
        aux_fx = fx
        print("IDIOMA: ",lang)
        print(len(set_audios[lang])+1)
        for audio in range(1,len(set_audios[lang])+1):


            if audio == 1:

                print("audio num:",audio)
                duration_audio = set_audios[lang][str(audio)].duration
                duration_video = set_videos[str(audio)].duration
                aux_temp = set_audios[lang][str(audio)]
                pausa = (duration_video - min(duration_audio, duration_video)) / 2

                
                aux_temp = aux_temp.subclipped(0, min(duration_audio, duration_video))
                aux_temp = aux_temp.with_start(pausa)
                aux_temp = aux_temp.with_end(pausa+min(duration_audio, duration_video))
                set_audios[lang][str(audio)] = aux_temp

                print("Timeline")
                print(aux_temp.start)
                print(aux_temp.end)
            else:
                print("audio num:",audio)
                duration_audio = set_audios[lang][str(audio)].duration
                duration_video = set_videos[str(audio)].duration
                aux_temp = set_audios[lang][str(audio)]
                pausa = (duration_video - min(duration_audio, duration_video)) / 2

                aux_temp = aux_temp.subclipped(0, min(duration_audio, duration_video))
                
                aux_temp = aux_temp.with_start(end_clip+pausa)
                aux_temp = aux_temp.with_end(end_clip+pausa+min(duration_audio, duration_video))
                set_audios[lang][str(audio)] = aux_temp
                print("Timeline")
                print(aux_temp.start)
                print(aux_temp.end)
            end_clip = pausa + aux_temp.end

        lista_audio_final = []
        print(set_audios[lang].keys())
        for i in set_audios[lang]:
            print(i)
            lista_audio_final.append(set_audios[lang][str(i)])
        print(lista_audio_final)
        narracao = CompositeAudioClip(lista_audio_final)
        print(narracao.start)
        print(narracao.end)
        narracao.close()
        

        print("Ajustando Audio FX......")
        aux_fx = aux_fx.with_effects([afx.AudioLoop(duration=narracao.duration)])
        aux_fx.close()

        print("Fechando audio completo......")
        audio_final = CompositeAudioClip([narracao, aux_fx])
        print(audio_final.start)
        print(audio_final.end)
        audio_final.close()

        print("Salvando Audio......")

        audio_final.write_audiofile(config["path_youtube_video"]+str(id)+"_"+lang+".mp3")
        audio_final.close()
        
        

    print("Montando completo......")
    # # Concatenar os vídeos com seus áudios
    lista_videos_final = []
    for i in set_videos:
        lista_videos_final.append(set_videos[i])
    final_video = concatenate_videoclips(lista_videos_final)

    final_video.close()


    # Redimensiona para 1920x1080
    print("Forçando Full HD......")
    
    final_video = final_video.with_effects([vfx.Resize((1920,1080))])
    print("Renderizando......")
    final_video = final_video.with_audio(audio_final)
    # final_video = final_video.with_effects([vfx.MultiplySpeed(0.95)])
    
    final_video.close()
    
    print("Salvando Mídia......")
    final_video.write_videofile(config["path_youtube_video"]+str(id)+".mp4")

if __name__ == "__main__":

    # print("Iniciando Edição .....")
    # parser = argparse.ArgumentParser(description="Configurações e input do id da historia")
    # parser.add_argument("id", type=str, help="ID da historia a qual será gerada as narrações")
    # parser.add_argument("--config", type=bool, help="Redefinir caminhos do projeto", default=False)

    # args = parser.parse_args()
    # print(f"ID História: {args.id}")
    # print(f"--config: {args.config}")

    # if args.config :
    #     utils.config()
    run("criancas_0")
