import requests
import json
from textwrap import fill

def obter_info_pokemon(nome_ou_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome_ou_id.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def obter_descricao_pokemon(nome_ou_id):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{nome_ou_id.lower()}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        for entry in data['flavor_text_entries']:
            if entry['language']['name'] == 'en':
                return entry['flavor_text'].replace('\n', ' ')
        return "Descrição não disponível"
    else:
        return "Descrição não encontrada"

def mostrar_pokemon(pokemon_data):
    print("\n" + "="*50)
    print(f"#{pokemon_data['id']} - {pokemon_data['name'].capitalize()}")
    print("="*50)
    
    tipos = [t['type']['name'] for t in pokemon_data['types']]
    print(f"Tipo(s): {', '.join(tipos)}")
    
    print("\nEstatísticas:")
    for stat in pokemon_data['stats']:
        print(f"{stat['stat']['name'].replace('-', ' ').title()}: {stat['base_stat']}")
    
    habilidades = [a['ability']['name'] for a in pokemon_data['abilities'] if not a['is_hidden']]
    habilidades_ocultas = [a['ability']['name'] for a in pokemon_data['abilities'] if a['is_hidden']]
    
    print("\nHabilidades:")
    print(", ".join(habilidades))
    if habilidades_ocultas:
        print(f"Habilidade Oculta: {', '.join(habilidades_ocultas)}")
    
    print(f"\nPeso: {pokemon_data['weight']/10} kg")
    print(f"Altura: {pokemon_data['height']/10} m")
    
    descricao = obter_descricao_pokemon(pokemon_data['name'])
    print("\nDescrição:")
    print(fill(descricao, width=50))
    print(pokemon_data['sprites']['front_default'])

def main():
    print("Bem-vindo à Pokédex do Terminal!")
    print("Digite 'sair' a qualquer momento para encerrar.\n")
    
    while True:
        entrada = input("Digite o nome ou número do Pokémon: ").strip()
        
        if entrada.lower() == 'sair':
            print("Até mais, Treinador!")
            break
        
        pokemon = obter_info_pokemon(entrada)
        
        if pokemon:
            mostrar_pokemon(pokemon)
        else:
            print(f"Pokémon '{entrada}' não encontrado. Tente novamente.")
        
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()