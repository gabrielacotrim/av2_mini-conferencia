from datetime import timedelta, datetime

def read_proposals(file_path):
    """lê o arquivo contendo a programação e retorna uma lista de tuplas (nome, duração)"""
    
    talks = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.endswith('min'):
                name, duration = line.rsplit(' ', 1)
                talks.append((name, int(duration[:-3])))
            elif line.endswith('lighting'):
                name = line.rsplit(' ', 1)[0]
                talks.append((name, 5))
    return talks


def format_time(start_time, duration_minutes):
    """formata a hora inicial e adiciona os minutos da duração"""
    end_time = start_time + timedelta(minutes=duration_minutes)
    return start_time.strftime('%H:%M'), end_time


def schedule_talks(talks, start_time, session_length):
    """organiza as palestras para uma sessão especifica,
    retorna as palestras agendadas e o horario final da sessao"""
   
    scheduled = []
    current_time = start_time
    total_duration = 0
    for talk in talks:
        if total_duration + talk[1] <= session_length:
            scheduled.append((current_time.strftime('%H:%M'), talk[0], talk[1]))
            current_time = current_time + timedelta(minutes=talk[1])
            total_duration += talk[1]
           
    remaining_talks = [talk for talk in talks if talk not in scheduled]
    return scheduled, remaining_talks


def main():
    # Configurações
    morning_start = datetime.strptime('09:00', '%H:%M')
    morning_length = 3 * 60     # 3 horas em  minutos
    afternoon_start = datetime.strptime('13:00', '%H:%M') 
    afternoon_length = 4 * 60    # 4 horas em minutos
    networking_start = datetime.strptime('16:00', '%H:%M')
    
    # lê as propostas das palestras
    talks = read_proposals(r'av2_mini-conferencia\mini_proposals.txt')
    
    # ordena as palestras por duração (decrescente para melhor encaixe)
    talks.sort(key=lambda x: x[1], reverse=True)
    
    # organiza a sessão da manhã
    morning_schedule, remaining_talks = schedule_talks(talks, morning_start, morning_length)
    
    # organiza a sessão da tarde
    afternoon_schedule, remaining_talks = schedule_talks(remaining_talks, afternoon_start, afternoon_length)
    
    # exibe o cronograma
    print("Track 1:")
    for time, title, duration in morning_schedule:
        print(f"{time} {title} {duration}min")
    print("12:00 Almoço")
    for time, title, duration in afternoon_schedule:
        print(f"{time} {title} {duration}min")
    print(f"{networking_start.strftime('%H:%M')} Evento de Networking")
    

if __name__ == '__main__':
    main()
