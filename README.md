'use client';

import { useState, useEffect } from 'react';

// ------------------------------------------------------------
// INTERFACES OBRIGATÓRIAS (tipos completos da API Pokémon TCG)
// ------------------------------------------------------------

export interface ResponsePokemonList {
  page: number;
  pageSize: number;
  count: number;
  totalCount: number;
  data: Pokemon[];
}

export interface Pokemon {
  id: string;
  name: string;
  supertype: string;
  subtypes: string[];
  level: string;
  hp: string;
  types: string[];
  evolvesFrom: string;
  abilities: Ability[];
  attacks: Attack[];
  weaknesses: Weakness[];
  resistances: Resistance[];
  retreatCost: string[];
  convertedRetreatCost: number;
  set: Set;
  number: string;
  artist: string;
  rarity: string;
  nationalPokedexNumbers: number[];
  legalities: Legalities;
  images: Images;
  tcgplayer: Tcgplayer;
  cardmarket: Cardmarket;
}

export interface Ability {
  name: string;
  text: string;
  type: string;
}

export interface Attack {
  name: string;
  cost: string[];
  convertedEnergyCost: number;
  damage: string;
  text: string;
}

export interface Weakness {
  type: string;
  value: string;
}

export interface Resistance {
  type: string;
  value: string;
}

export interface Set {
  id: string;
  name: string;
  series: string;
  printedTotal: number;
  total: number;
  legalities: Legalities;
  ptcgoCode: string;
  releaseDate: string;
  updatedAt: string;
  images: Images;
}

export interface Legalities {
  unlimited: string;
}

export interface Images {
  symbol?: string;
  logo?: string;
  large: string;
  small: string;
}

export interface Tcgplayer {
  url: string;
  updatedAt: string;
  prices: Prices;
}

export interface Prices {
  holofoil?: Holofoil;
  reverseHolofoil?: ReverseHolofoil;
}

export interface Holofoil {
  low: number;
  mid: number;
  high: number;
  market: number;
  directLow: number;
}

export interface ReverseHolofoil {
  low: number;
  mid: number;
  high: number;
  market: number;
  directLow: unknown;
}

export interface Cardmarket {
  url: string;
  updatedAt: string;
  prices: Prices;
}

// ------------------------------------------------------------
// COMPONENTE PRINCIPAL
// ------------------------------------------------------------

export default function PokedexPage() {
  const [cards, setCards] = useState<Pokemon[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Função para buscar as cartas
  const fetchCards = async (query = '') => {
    setLoading(true);
    setError('');

    try {
      const url = query
        ? `https://api.pokemontcg.io/v2/cards?q=name:${query}&orderBy=number,name&perPage=15`
        : `https://api.pokemontcg.io/v2/cards?page=1&pageSize=15`;

      const res = await fetch(url);
      const data: ResponsePokemonList = await res.json();

      if (data && data.data) {
        setCards(data.data);
      } else {
        setError('Nenhuma carta encontrada.');
      }
    } catch (err) {
      console.error(err);
      setError('Erro ao buscar cartas.');
    } finally {
      setLoading(false);
    }
  };

  // Busca inicial
  useEffect(() => {
    fetchCards();
  }, []);

  // Formulário de busca
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchCards(search.trim());
  };

  // ------------------------------------------------------------
  // RENDERIZAÇÃO
  // ------------------------------------------------------------
  return (
    <div className="min-h-screen flex flex-col items-center justify-start bg-gradient-to-b from-yellow-300 via-orange-400 to-red-500 text-gray-900 p-6">
      <div className="bg-white/90 backdrop-blur-md shadow-xl rounded-2xl p-8 w-full max-w-6xl">
        <h1 className="text-3xl font-bold text-center text-red-600 mb-2">
          Pokémon TCG Explorer
        </h1>
        <p className="text-center text-gray-600 mb-6">
          Pesquise e explore cartas do universo Pokémon!
        </p>

        {/* Formulário de busca */}
        <form onSubmit={handleSearch} className="flex justify-center gap-3 mb-8">
          <input
            type="text"
            placeholder="Digite o nome do Pokémon..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="p-3 rounded-lg w-2/3 border border-gray-300 outline-none focus:ring-2 focus:ring-red-400"
          />
          <button
            type="submit"
            className="bg-red-600 hover:bg-red-700 text-white px-5 py-3 rounded-lg font-semibold transition"
          >
            Buscar
          </button>
        </form>

        {/* Mensagens */}
        {loading && <p className="text-center text-gray-700">Carregando cartas...</p>}
        {error && <p className="text-center text-red-500">{error}</p>}

        {/* Grade de cartas */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {cards.map((card) => (
            <div
              key={card.id}
              className="bg-white border border-gray-200 rounded-xl shadow-md hover:shadow-xl transition p-3"
            >
              <img
                src={card.images.small}
                alt={card.name}
                className="rounded-md mx-auto mb-2 w-full h-64 object-contain"
              />
              <h2 className="text-lg font-bold text-gray-800 text-center">
                #{card.number} - {card.name}
              </h2>
              <p className="text-sm text-center text-gray-500">
                HP: {card.hp || '??'}{' '}
                {card.types && <span>({card.types.join(', ')})</span>}
              </p>
              <p className="text-center mt-2 text-sm text-gray-600 italic">
                {card.rarity || 'Sem raridade'}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
} Dashboard de Salários na Área de Dados

Este projeto é um **dashboard interativo** desenvolvido com [Streamlit](https://streamlit.io/), que permite explorar dados salariais na área de dados ao redor do mundo.  
Ele oferece filtros dinâmicos, gráficos interativos e métricas principais para facilitar a análise.

---

## 🚀 Funcionalidades

- 🔍 **Filtros interativos** na barra lateral:
  - Ano
  - Senioridade
  - Tipo de contrato
  - Tamanho da empresa  

- 📈 **Visualizações dinâmicas**:
  - Top 10 cargos por salário médio
  - Distribuição de salários anuais
  - Proporção dos tipos de trabalho (remoto, híbrido, presencial)
  - Salário médio de Cientistas de Dados por país (mapa interativo)

- 📊 **Métricas principais (KPIs)**:
  - Salário médio
  - Salário máximo
  - Total de registros
  - Cargo mais frequente

- 📑 **Tabela detalhada** com os dados filtrados.

---

## 🛠️ Tecnologias utilizadas

- [Python 3](https://www.python.org/)  
- [Pandas](https://pandas.pydata.org/) – tratamento de dados  
- [Plotly Express](https://plotly.com/python/plotly-express/) – gráficos interativos  
- [Streamlit](https://streamlit.io/) – construção do dashboard  

---

## 📂 Estrutura do projeto

