'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // --- Lógica de login lendo variáveis do .env ---
    const emailCorreto = process.env.NEXT_PUBLIC_TEST_EMAIL;
    const senhaCorreta = process.env.NEXT_PUBLIC_TEST_PASSWORD;

    if (email === emailCorreto && password === senhaCorreta) {
      const token = 'token-simulado-login-ok';
      localStorage.setItem('token', token);
      localStorage.setItem('username', email);
      router.push('/blackjack');
    } else {
      setError('E-mail ou senha inválidos.');
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-green-300 via-blue-400 to-blue-600 p-6">
      <div className="bg-white/90 backdrop-blur-sm border border-white/50 rounded-2xl shadow-xl p-8 w-full max-w-md text-center">
        <h1 className="text-3xl font-bold mb-2 text-blue-800">
          Pokémon TCG Explorer
        </h1>
        <p className="text-gray-600 mb-6">Faça login para continuar</p>

        <form onSubmit={handleLogin} className="flex flex-col gap-4">
          <input
            type="email"
            placeholder="Seu e-mail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="p-3 rounded-md border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
          />

          <input
            type="password"
            placeholder="Sua senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="p-3 rounded-md border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
          />

          {error && <p className="text-red-500 text-sm">{error}</p>}

          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-md transition"
          >
            Entrar
          </button>
        </form>

        <p className="mt-6 text-sm text-gray-500">
          © 2025 Pokémon TCG Explorer. Todos os direitos reservados.
        </p>
      </div>
    </div>
  );
}












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
}