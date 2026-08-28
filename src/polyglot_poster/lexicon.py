"""Fifteen everyday situations. Column order is always

    English / Spanish / Portuguese / Italian / French / Korean
"""

from __future__ import annotations

from polyglot_poster.vocab import VOCAB

LANGS = ("en", "es", "pt", "it", "fr", "ko")

LANG_LABELS = {
    "en": "English",
    "es": "Spanish",
    "pt": "Portuguese",
    "it": "Italian",
    "fr": "French",
    "ko": "Korean",
}

LANG_NATIVE = {
    "en": "English",
    "es": "Español",
    "pt": "Português",
    "it": "Italiano",
    "fr": "Français",
    "ko": "한국어",
}


def _t(en: str, es: str, pt: str, it: str, fr: str, ko: str) -> dict[str, str]:
    return {"en": en, "es": es, "pt": pt, "it": it, "fr": fr, "ko": ko}


def _cat(
    *,
    id: str,
    color: str,
    source: str,
    titles: dict[str, str],
    vocab: list[dict[str, str]],
    phrases: list[dict[str, str]],
) -> dict:
    if len(phrases) != 3:
        raise ValueError(f"{id}: need 3 phrases, got {len(phrases)}")
    return {
        "id": id,
        "color": color,
        "source": source,
        "titles": titles,
        "vocab": vocab,
        "phrases": phrases,
    }


CATEGORIES: list[dict] = [
    _cat(
        id="restaurant",
        color="#C44B32",
        source="IMG_1502 · p. 9 (flap of p. 10 is folded over, upside down)",
        titles=_t(
            "At the restaurant",
            "En el restaurante",
            "No restaurante",
            "Al ristorante",
            "Au restaurant",
            "식당에서",
        ),
        vocab=VOCAB["restaurant"],
        phrases=[
            _t(
                "Could we have the bill, please?",
                "¿Nos trae la cuenta, por favor?",
                "Pode trazer a conta, por favor?",
                "Ci porta il conto, per favore?",
                "On pourrait avoir l'addition, s'il vous plaît ?",
                "계산서 주시겠어요?",
            ),
            _t(
                "I'll have the roast chicken and a glass of wine.",
                "Para mí el pollo asado y una copa de vino.",
                "Eu quero o frango assado e uma taça de vinho.",
                "Prendo il pollo arrosto e un bicchiere di vino.",
                "Je prendrai le poulet rôti et un verre de vin.",
                "구운 닭고기에 와인 한 잔 주세요.",
            ),
            _t(
                "Is this dish vegetarian?",
                "¿Este plato es vegetariano?",
                "Esse prato é vegetariano?",
                "Questo piatto è vegetariano?",
                "Ce plat est végétarien ?",
                "이 요리 채식이에요?",
            ),
        ],
    ),
    _cat(
        id="store",
        color="#7A378A",
        source="IMG_1501 · ch. 3 · p. 18",
        titles=_t(
            "At the Department Store",
            "En los grandes almacenes",
            "Na loja de departamentos",
            "Al grande magazzino",
            "Au grand magasin",
            "백화점에서",
        ),
        vocab=VOCAB["store"],
        phrases=[
            _t(
                "Excuse me, where is the clothing department?",
                "Perdón, ¿dónde está la sección de ropa?",
                "Com licença, onde fica a seção de roupas?",
                "Scusi, dov'è il reparto abbigliamento?",
                "Pardon, où est le rayon vêtements ?",
                "죄송한데, 의류 매장은 어디에 있어요?",
            ),
            _t(
                "Do you have this dress in a smaller size?",
                "¿Tienen este vestido en una talla más pequeña?",
                "Vocês têm este vestido num tamanho menor?",
                "Avete questo vestito in una taglia più piccola?",
                "Vous avez cette robe dans une taille plus petite ?",
                "이 원피스 더 작은 사이즈 있어요?",
            ),
            _t(
                "I'll take it. Can I pay by card?",
                "Me lo llevo. ¿Puedo pagar con tarjeta?",
                "Vou levar. Posso pagar com cartão?",
                "Lo prendo. Posso pagare con la carta?",
                "Je la prends. Je peux payer par carte ?",
                "이걸로 할게요. 카드로 결제돼요?",
            ),
        ],
    ),
    _cat(
        id="airport",
        color="#2A6CB0",
        source="IMG_1503 · ch. 4 · p. 30",
        titles=_t(
            "At the airport",
            "En el aeropuerto",
            "No aeroporto",
            "All'aeroporto",
            "À l'aéroport",
            "공항에서",
        ),
        vocab=VOCAB["airport"],
        phrases=[
            _t(
                "Where is the gate for the flight to Paris?",
                "¿Dónde está la puerta del vuelo a París?",
                "Onde fica o portão do voo para Paris?",
                "Dov'è il gate del volo per Parigi?",
                "Où est la porte d'embarquement pour le vol vers Paris ?",
                "파리행 비행기 탑승구가 어디예요?",
            ),
            _t(
                "I'd like a window seat, please.",
                "Quisiera un asiento de ventanilla, por favor.",
                "Eu queria um assento na janela, por favor.",
                "Vorrei un posto finestrino, per favore.",
                "Je voudrais une place côté hublot, s'il vous plaît.",
                "창가 자리로 주세요.",
            ),
            _t(
                "I have nothing to declare.",
                "No tengo nada que declarar.",
                "Não tenho nada a declarar.",
                "Non ho nulla da dichiarare.",
                "Je n'ai rien à déclarer.",
                "신고할 물건은 없습니다.",
            ),
        ],
    ),
    _cat(
        id="family",
        color="#C44768",
        source="IMG_1498 · ch. 5 · p. 40",
        titles=_t(
            "The family",
            "La familia",
            "A família",
            "La famiglia",
            "La famille",
            "가족",
        ),
        vocab=VOCAB["family"],
        phrases=[
            _t(
                "This is my older sister and her husband.",
                "Esta es mi hermana mayor y su marido.",
                "Esta é a minha irmã mais velha e o marido dela.",
                "Questa è mia sorella maggiore e suo marito.",
                "Voici ma sœur aînée et son mari.",
                "이쪽은 제 언니와 형부예요.",
            ),
            _t(
                "We're having dinner at my grandparents' on Sunday.",
                "El domingo cenamos en casa de mis abuelos.",
                "No domingo vamos jantar na casa dos meus avós.",
                "Domenica ceniamo dai nonni.",
                "Dimanche on dîne chez mes grands-parents.",
                "일요일에 조부모님 댁에서 저녁 먹어요.",
            ),
            _t(
                "How many children do you have?",
                "¿Cuántos hijos tienen?",
                "Vocês têm quantos filhos?",
                "Quanti figli avete?",
                "Vous avez combien d'enfants ?",
                "자녀가 몇 명이에요?",
            ),
        ],
    ),
    _cat(
        id="hotel",
        color="#1A8A82",
        source="IMG_1505 · ch. 6 · p. 67",
        titles=_t(
            "At the hotel",
            "En el hotel",
            "No hotel",
            "In albergo",
            "À l'hôtel",
            "호텔에서",
        ),
        vocab=VOCAB["hotel"],
        phrases=[
            _t(
                "I have a reservation under the name Martin.",
                "Tengo una reserva a nombre de Martin.",
                "Tenho uma reserva no nome Martin.",
                "Ho una prenotazione a nome Martin.",
                "J'ai une réservation au nom de Martin.",
                "마틴 이름으로 예약했는데요.",
            ),
            _t(
                "What time is breakfast?",
                "¿A qué hora es el desayuno?",
                "A que horas é o café da manhã?",
                "A che ora è la colazione?",
                "Le petit-déjeuner est à quelle heure ?",
                "아침 식사는 몇 시예요?",
            ),
            _t(
                "Could I have a quieter room? This one is too noisy.",
                "¿Me podría dar una habitación más tranquila? Esta es muy ruidosa.",
                "Poderia me dar um quarto mais silencioso? Este é barulhento demais.",
                "Potrei avere una camera più silenziosa? Questa è troppo rumorosa.",
                "Je pourrais avoir une chambre plus calme ? Celle-ci est trop bruyante.",
                "더 조용한 방으로 바꿔 주실 수 있어요? 여기가 너무 시끄러워요.",
            ),
        ],
    ),
    _cat(
        id="birthday",
        color="#C43A86",
        source="IMG_1506 · ch. 7 · p. 76",
        titles=_t(
            "A birthday party",
            "Una fiesta de cumpleaños",
            "Uma festa de aniversário",
            "Una festa di compleanno",
            "Une fête d'anniversaire",
            "생일 파티",
        ),
        vocab=VOCAB["birthday"],
        phrases=[
            _t(
                "Happy birthday! I brought you a small gift.",
                "¡Feliz cumpleaños! Te traje un regalito.",
                "Feliz aniversário! Trouxe um presentinho para você.",
                "Buon compleanno! Ti ho portato un piccolo regalo.",
                "Joyeux anniversaire ! Je t'ai apporté un petit cadeau.",
                "생일 축하해! 작은 선물 가져왔어.",
            ),
            _t(
                "Blow out the candles and make a wish.",
                "Sopla las velas y pide un deseo.",
                "Sopra as velas e faça um pedido.",
                "Soffia le candeline e fai un desiderio.",
                "Souffle les bougies et fais un vœu.",
                "촛불을 끄고 소원을 빌어.",
            ),
            _t(
                "Thanks for coming to the party.",
                "Gracias por venir a la fiesta.",
                "Obrigado por ter vindo à festa.",
                "Grazie di essere venuti alla festa.",
                "Merci d'être venus à la fête.",
                "파티에 와 줘서 고마워.",
            ),
        ],
    ),
    _cat(
        id="grocery",
        color="#3D8A32",
        source="IMG_1507 · ch. 8",
        titles=_t(
            "The corner grocery",
            "La tienda de la esquina",
            "O mercado da esquina",
            "L'alimentari all'angolo",
            "L'épicerie du coin",
            "동네 식료품점",
        ),
        vocab=VOCAB["grocery"],
        phrases=[
            _t(
                "A baguette and half a kilo of tomatoes, please.",
                "Una barra de pan y medio kilo de tomates, por favor.",
                "Uma baguete e meio quilo de tomates, por favor.",
                "Una baguette e mezzo chilo di pomodori, per favore.",
                "Une baguette et un demi-kilo de tomates, s'il vous plaît.",
                "바게트 하나랑 토마토 500그램 주세요.",
            ),
            _t(
                "Where can I find the olive oil?",
                "¿Dónde está el aceite de oliva?",
                "Onde fica o azeite?",
                "Dov'è l'olio d'oliva?",
                "Où est l'huile d'olive ?",
                "올리브유는 어디에 있어요?",
            ),
            _t(
                "Do you have change for a twenty?",
                "¿Me puede cambiar un billete de veinte?",
                "Tem troco para uma nota de vinte?",
                "Ha il resto per una banconota da venti?",
                "Vous avez la monnaie sur un billet de vingt ?",
                "이십 유로짜리 잔돈 있으세요?",
            ),
        ],
    ),
    _cat(
        id="bank",
        color="#C49220",
        source="IMG_1508 · ch. 9 · p. 100",
        titles=_t(
            "At the bank",
            "En el banco",
            "No banco",
            "In banca",
            "À la banque",
            "은행에서",
        ),
        vocab=VOCAB["bank"],
        phrases=[
            _t(
                "I'd like to open a checking account.",
                "Quisiera abrir una cuenta corriente.",
                "Eu gostaria de abrir uma conta corrente.",
                "Vorrei aprire un conto corrente.",
                "Je voudrais ouvrir un compte courant.",
                "입출금 계좌를 개설하고 싶어요.",
            ),
            _t(
                "I need to withdraw cash from the ATM.",
                "Necesito sacar dinero del cajero.",
                "Preciso sacar dinheiro no caixa eletrônico.",
                "Devo prelevare contanti al bancomat.",
                "Je dois retirer de l'argent au distributeur.",
                "ATM에서 현금을 뽑아야 해요.",
            ),
            _t(
                "What's the exchange rate for dollars?",
                "¿Cuál es el tipo de cambio del dólar?",
                "Qual é a cotação do dólar?",
                "Qual è il cambio del dollaro?",
                "Quel est le taux de change pour les dollars ?",
                "달러 환율이 어떻게 돼요?",
            ),
        ],
    ),
    _cat(
        id="train",
        color="#3B3F8C",
        source="IMG_1509 · ch. 10 · p. 111",
        titles=_t(
            "At the railroad station",
            "En la estación de tren",
            "Na estação de trem",
            "In stazione",
            "À la gare",
            "기차역에서",
        ),
        vocab=VOCAB["train"],
        phrases=[
            _t(
                "Which platform for the train to Lyon?",
                "¿De qué andén sale el tren a Lyon?",
                "De qual plataforma sai o trem para Lyon?",
                "Da quale binario parte il treno per Lione?",
                "C'est quel quai pour le train pour Lyon ?",
                "리옹 가는 기차는 몇 번 승강장이에요?",
            ),
            _t(
                "Is this seat free?",
                "¿Está libre este asiento?",
                "Este assento está livre?",
                "È libero questo posto?",
                "Cette place est libre ?",
                "이 자리 비어 있어요?",
            ),
            _t(
                "We missed our connection. When is the next train?",
                "Perdimos el enlace. ¿Cuándo es el próximo tren?",
                "Perdemos a conexão. Quando é o próximo trem?",
                "Abbiamo perso la coincidenza. Quando c'è il prossimo treno?",
                "On a raté la correspondance. C'est quand, le prochain train ?",
                "환승을 놓쳤어요. 다음 기차는 언제예요?",
            ),
        ],
    ),
    _cat(
        id="body",
        color="#D15A3A",
        source="IMG_1510 · ch. 11 · p. 140",
        titles=_t(
            "Parts of the body",
            "Las partes del cuerpo",
            "As partes do corpo",
            "Le parti del corpo",
            "Les parties du corps",
            "신체 부위",
        ),
        vocab=VOCAB["body"],
        phrases=[
            _t(
                "My throat hurts and I have a fever.",
                "Me duele la garganta y tengo fiebre.",
                "Estou com dor de garganta e febre.",
                "Ho mal di gola e la febbre.",
                "J'ai mal à la gorge et de la fièvre.",
                "목이 아프고 열이 나요.",
            ),
            _t(
                "I twisted my ankle on the stairs.",
                "Me torcí el tobillo en las escaleras.",
                "Torci o tornozelo na escada.",
                "Mi sono storciata la caviglia sulle scale.",
                "Je me suis tordu la cheville dans l'escalier.",
                "계단에서 발목을 접질렀어요.",
            ),
            _t(
                "Take a deep breath, please.",
                "Respire hondo, por favor.",
                "Respire fundo, por favor.",
                "Faccia un bel respiro, per favore.",
                "Respirez profondément, s'il vous plaît.",
                "깊게 숨 쉬어 보세요.",
            ),
        ],
    ),
    _cat(
        id="health",
        color="#2E9A72",
        source="IMG_1500 · p. 151",
        titles=_t(
            "Health and grooming",
            "Salud y aseo",
            "Saúde e higiene",
            "Salute e cura di sé",
            "Santé et toilette",
            "건강과 몸단장",
        ),
        vocab=VOCAB["health"],
        phrases=[
            _t(
                "I need an appointment with the doctor.",
                "Necesito una cita con el médico.",
                "Preciso marcar uma consulta com o médico.",
                "Ho bisogno di un appuntamento dal medico.",
                "Il me faut un rendez-vous chez le médecin.",
                "의사 선생님 예약을 하고 싶어요.",
            ),
            _t(
                "Can you fill this prescription?",
                "¿Me puede preparar esta receta?",
                "Pode preparar esta receita?",
                "Mi può preparare questa ricetta?",
                "Vous pouvez me préparer cette ordonnance ?",
                "이 처방전 조제해 주시겠어요?",
            ),
            _t(
                "I've been coughing for three days.",
                "Llevo tres días tosiendo.",
                "Estou tossindo há três dias.",
                "Tosso da tre giorni.",
                "Je tousse depuis trois jours.",
                "사흘째 기침이 나요.",
            ),
        ],
    ),
    _cat(
        id="car",
        color="#4A5560",
        source="IMG_1511 · p. 161",
        titles=_t(
            "The automobile",
            "El automóvil",
            "O automóvel",
            "L'automobile",
            "La voiture",
            "자동차",
        ),
        vocab=VOCAB["car"],
        phrases=[
            _t(
                "I have a flat tire. Is there a gas station nearby?",
                "Se me pinchó una rueda. ¿Hay una gasolinera cerca?",
                "O pneu furou. Tem um posto por perto?",
                "Ho una gomma a terra. C'è un distributore qui vicino?",
                "J'ai un pneu crevé. Il y a une station-service près d'ici ?",
                "타이어가 펑크 났어요. 근처에 주유소 있어요?",
            ),
            _t(
                "Fill it up, please. Unleaded.",
                "Lleno, por favor. Sin plomo.",
                "Completa, por favor. Gasolina comum.",
                "Il pieno, per favore. Senza piombo.",
                "Le plein, s'il vous plaît. Sans plomb.",
                "가득 넣어 주세요. 무연 휘발유요.",
            ),
            _t(
                "I got a parking ticket.",
                "Me pusieron una multa de aparcamiento.",
                "Levei uma multa de estacionamento.",
                "Ho preso una multa per sosta vietata.",
                "J'ai pris une contravention pour le stationnement.",
                "주차 벌금 딱지를 뗐어요.",
            ),
        ],
    ),
    _cat(
        id="computers",
        color="#2C62B8",
        source="IMG_1504 · p. 172",
        titles=_t(
            "Computers",
            "Informática",
            "Informática",
            "Informatica",
            "L'informatique",
            "컴퓨터",
        ),
        vocab=VOCAB["computers"],
        phrases=[
            _t(
                "I forgot my password again.",
                "Se me olvidó otra vez la contraseña.",
                "Esqueci a senha de novo.",
                "Ho di nuovo dimenticato la password.",
                "J'ai encore oublié mon mot de passe.",
                "또 비밀번호를 잊어버렸어요.",
            ),
            _t(
                "Could you print this document for me?",
                "¿Me puede imprimir este documento?",
                "Pode imprimir este documento para mim?",
                "Mi può stampare questo documento?",
                "Vous pouvez m'imprimer ce document ?",
                "이 문서 출력해 주시겠어요?",
            ),
            _t(
                "The wifi isn't working in my room.",
                "El wifi no funciona en mi habitación.",
                "O wi-fi não funciona no meu quarto.",
                "Il wifi non funziona in camera mia.",
                "Le wifi ne marche pas dans ma chambre.",
                "제 방에서 와이파이가 안 돼요.",
            ),
        ],
    ),
    _cat(
        id="clothes",
        color="#8B2A48",
        source="proposed — the store chapter is furniture-heavy; learners still need a wardrobe",
        titles=_t(
            "Clothes",
            "La ropa",
            "A roupa",
            "I vestiti",
            "Les vêtements",
            "옷",
        ),
        vocab=VOCAB["clothes"],
        phrases=[
            _t(
                "It looks great on you. You should take it.",
                "Te queda genial. Deberías llevártelo.",
                "Fica ótimo em você. Acho que deve levar.",
                "Ti sta benissimo. Dovresti prenderlo.",
                "Ça te va très bien. Tu devrais la prendre.",
                "잘 어울려요. 이거 사시는 게 좋겠어요.",
            ),
            _t(
                "I'm looking for a black jacket for a wedding.",
                "Busco una chaqueta negra para una boda.",
                "Estou procurando uma jaqueta preta para um casamento.",
                "Cerco una giacca nera per un matrimonio.",
                "Je cherche une veste noire pour un mariage.",
                "결혼식에 입을 검은 재킷을 찾고 있어요.",
            ),
            _t(
                "These shoes are too tight. Do you have a larger size?",
                "Estos zapatos me están estrechos. ¿Tienen una talla más grande?",
                "Este sapato está apertado. Tem um tamanho maior?",
                "Queste scarpe sono troppo strette. Avete una taglia più grande?",
                "Ces chaussures sont trop étroites. Vous avez une taille au-dessus ?",
                "이 신발 너무 끼어요. 한 치수 큰 거 있어요?",
            ),
        ],
    ),
    _cat(
        id="weather",
        color="#1A9BB0",
        source="proposed — plus déjà / maintenant / depuis from the upside-down flap of IMG_1502",
        titles=_t(
            "Weather",
            "El tiempo que hace",
            "O tempo que faz",
            "Il tempo che fa",
            "Le temps qu'il fait",
            "날씨",
        ),
        vocab=VOCAB["weather"],
        phrases=[
            _t(
                "It's pouring. Did you bring an umbrella?",
                "Está lloviendo a cántaros. ¿Trajiste paraguas?",
                "Está caindo um dilúvio. Você trouxe guarda-chuva?",
                "Sta piovendo a dirotto. Hai portato l'ombrello?",
                "Il pleut des cordes. T'as pris un parapluie ?",
                "비가 엄청 와요. 우산 가져왔어요?",
            ),
            _t(
                "Tomorrow will be sunny and a bit chilly.",
                "Mañana hará sol y un poco de fresco.",
                "Amanhã vai estar ensolarado e um pouco fresco.",
                "Domani sarà soleggiato e un po' fresco.",
                "Demain il fera soleil, un peu frais.",
                "내일은 맑고 조금 쌀쌀하대요.",
            ),
            _t(
                "What time does it get dark here?",
                "¿A qué hora anochece aquí?",
                "A que horas escurece aqui?",
                "A che ora fa buio qui?",
                "Il fait nuit à quelle heure, ici ?",
                "여기는 몇 시에 어두워져요?",
            ),
        ],
    ),
]


def validate() -> None:
    if len(CATEGORIES) != 15:
        raise AssertionError(f"need 15 categories for 3 rows of 5, got {len(CATEGORIES)}")
    for cat in CATEGORIES:
        if len(cat["phrases"]) != 3:
            raise AssertionError(cat["id"])
        if len(cat["vocab"]) < 40:
            raise AssertionError(f"{cat['id']} only {len(cat['vocab'])} words")
        for row in cat["vocab"] + cat["phrases"] + [cat["titles"]]:
            missing = [lang for lang in LANGS if lang not in row or not row[lang].strip()]
            if missing:
                raise AssertionError(f"{cat['id']} missing {missing}")
