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
                "Could we have the bill when you have a moment, please?",
                "¿Nos trae la cuenta cuando pueda, por favor?",
                "Pode trazer a conta quando puder, por favor?",
                "Ci porta il conto quando ha un momento, per favore?",
                "On pourrait avoir l'addition quand vous aurez un moment, s'il vous plaît ?",
                "잠깐 시간 되실 때 계산서 주시겠어요?",
            ),
            _t(
                "I'll have the roast chicken, a salad, and a glass of red wine.",
                "Para mí el pollo asado, una ensalada y una copa de vino tinto.",
                "Eu quero o frango assado, uma salada e uma taça de vinho tinto.",
                "Prendo il pollo arrosto, un'insalata e un bicchiere di vino rosso.",
                "Je prendrai le poulet rôti, une salade et un verre de vin rouge.",
                "구운 닭고기랑 샐러드에 레드 와인 한 잔 주세요.",
            ),
            _t(
                "Is this dish vegetarian, or does the sauce have meat or fish in it?",
                "¿Este plato es vegetariano, o la salsa lleva carne o pescado?",
                "Esse prato é vegetariano, ou o molho tem carne ou peixe?",
                "Questo piatto è vegetariano, o nel sugo c'è carne o pesce?",
                "Ce plat est végétarien, ou la sauce contient de la viande ou du poisson ?",
                "이 요리 채식이에요, 아니면 소스에 고기나 생선이 들어 있어요?",
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
                "Excuse me, where's the clothing department on this floor?",
                "Perdón, ¿dónde está la sección de ropa en esta planta?",
                "Com licença, onde fica a seção de roupas neste andar?",
                "Scusi, dov'è il reparto abbigliamento su questo piano?",
                "Pardon, où est le rayon vêtements à cet étage ?",
                "죄송한데, 이 층 의류 매장은 어디에 있어요?",
            ),
            _t(
                "Do you have this dress in a smaller size, maybe in navy?",
                "¿Tienen este vestido en una talla más pequeña, quizá en azul marino?",
                "Vocês têm este vestido num tamanho menor, talvez em azul-marinho?",
                "Avete questo vestito in una taglia più piccola, magari in blu scuro?",
                "Vous avez cette robe dans une taille plus petite, peut-être en marine ?",
                "이 원피스 더 작은 사이즈 있어요? 네이비로요.",
            ),
            _t(
                "I'll take it. Can I pay by card, or do you only take cash?",
                "Me lo llevo. ¿Puedo pagar con tarjeta, o solo aceptan efectivo?",
                "Vou levar. Posso pagar com cartão, ou vocês só aceitam dinheiro?",
                "Lo prendo. Posso pagare con la carta, o accettate solo contanti?",
                "Je la prends. Je peux payer par carte, ou vous ne prenez que des espèces ?",
                "이걸로 할게요. 카드로 결제돼요, 아니면 현금만 돼요?",
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
                "Where is the gate for the afternoon flight to Paris, please?",
                "¿Dónde está la puerta del vuelo de la tarde a París, por favor?",
                "Onde fica o portão do voo da tarde para Paris, por favor?",
                "Dov'è il gate del volo pomeridiano per Parigi, per favore?",
                "Où est la porte d'embarquement pour le vol de l'après-midi vers Paris ?",
                "오후 파리행 비행기 탑승구가 어디예요?",
            ),
            _t(
                "I'd like a window seat toward the front of the plane, please.",
                "Quisiera un asiento de ventanilla hacia adelante, por favor.",
                "Eu queria um assento na janela, mais na frente do avião, por favor.",
                "Vorrei un posto finestrino verso la parte anteriore, per favore.",
                "Je voudrais une place côté hublot vers l'avant de l'appareil, s'il vous plaît.",
                "앞쪽 창가 자리로 주세요.",
            ),
            _t(
                "I have nothing to declare; it's only clothes and a few books.",
                "No tengo nada que declarar; solo son ropa y unos libros.",
                "Não tenho nada a declarar; é só roupa e alguns livros.",
                "Non ho nulla da dichiarare; sono solo vestiti e qualche libro.",
                "Je n'ai rien à déclarer ; ce n'est que des vêtements et quelques livres.",
                "신고할 물건은 없습니다. 옷이랑 책 몇 권뿐이에요.",
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
                "This is my older sister and her husband; they live nearby.",
                "Esta es mi hermana mayor y su marido; viven aquí cerca.",
                "Esta é a minha irmã mais velha e o marido dela; eles moram aqui perto.",
                "Questa è mia sorella maggiore e suo marito; abitano qui vicino.",
                "Voici ma sœur aînée et son mari ; ils habitent tout près d'ici.",
                "이쪽은 제 언니와 형부예요. 근처에 살아요.",
            ),
            _t(
                "We're having dinner at my grandparents' house on Sunday evening.",
                "El domingo por la noche cenamos en casa de mis abuelos.",
                "No domingo à noite vamos jantar na casa dos meus avós.",
                "Domenica sera ceniamo a casa dei nonni.",
                "Dimanche soir on dîne chez mes grands-parents.",
                "일요일 저녁에 조부모님 댁에서 저녁 먹어요.",
            ),
            _t(
                "How many children do you two have, if you don't mind my asking?",
                "¿Cuántos hijos tienen ustedes, si no es indiscreción preguntar?",
                "Vocês dois têm quantos filhos, se não for indiscrição perguntar?",
                "Quanti figli avete voi due, se posso permettermi di chiedere?",
                "Vous avez combien d'enfants tous les deux, si ce n'est pas indiscret ?",
                "두 분은 자녀가 몇 명이에요? 물어봐도 괜찮죠?",
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
                "Hello, I have a reservation under the name Martin for two nights.",
                "Hola, tengo una reserva a nombre de Martin para dos noches.",
                "Olá, tenho uma reserva no nome Martin para duas noites.",
                "Buonasera, ho una prenotazione a nome Martin per due notti.",
                "Bonjour, j'ai une réservation au nom de Martin pour deux nuits.",
                "안녕하세요, 마틴 이름으로 이틀 예약했는데요.",
            ),
            _t(
                "What time is breakfast served, and is it included in the room?",
                "¿A qué hora es el desayuno, y está incluido en la habitación?",
                "A que horas é o café da manhã, e está incluso no quarto?",
                "A che ora è la colazione, ed è inclusa nella camera?",
                "Le petit-déjeuner est à quelle heure, et il est compris dans la chambre ?",
                "아침 식사는 몇 시예요, 객실 요금에 포함인가요?",
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
                "Happy birthday! I brought you a small gift I thought you'd like.",
                "¡Feliz cumpleaños! Te traje un regalito que pensé que te gustaría.",
                "Feliz aniversário! Trouxe um presentinho que achei que você ia gostar.",
                "Buon compleanno! Ti ho portato un piccolo regalo che pensavo ti piacesse.",
                "Joyeux anniversaire ! Je t'ai apporté un petit cadeau que tu aimeras, je crois.",
                "생일 축하해! 네가 좋아할 것 같아서 작은 선물 가져왔어.",
            ),
            _t(
                "Go on, blow out the candles and make a wish before they melt.",
                "Venga, sopla las velas y pide un deseo antes de que se derritan.",
                "Vamos, sopra as velas e faça um pedido antes que derretam.",
                "Dai, soffia le candeline e fai un desiderio prima che si sciolgano.",
                "Allez, souffle les bougies et fais un vœu avant qu'elles ne fondent.",
                "자, 촛불 녹기 전에 끄고 소원 빌어.",
            ),
            _t(
                "Thanks so much for coming tonight; it wouldn't be the same without you.",
                "Gracias de verdad por venir esta noche; no sería lo mismo sin ustedes.",
                "Muito obrigado por ter vindo hoje à noite; não seria igual sem vocês.",
                "Grazie di cuore per essere venuti stasera; senza di voi non sarebbe lo stesso.",
                "Merci beaucoup d'être venus ce soir ; ça ne serait pas pareil sans vous.",
                "오늘 밤 와 줘서 정말 고마워. 너희가 없었으면 달랐을 거야.",
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
                "A baguette and half a kilo of tomatoes, please, and that's all.",
                "Una barra de pan y medio kilo de tomates, por favor, y nada más.",
                "Uma baguete e meio quilo de tomates, por favor, e só isso.",
                "Una baguette e mezzo chilo di pomodori, per favore, e basta.",
                "Une baguette et un demi-kilo de tomates, s'il vous plaît, et ce sera tout.",
                "바게트 하나랑 토마토 500그램만 주세요.",
            ),
            _t(
                "Sorry, where can I find the olive oil? I already looked on that shelf.",
                "Perdón, ¿dónde está el aceite de oliva? Ya miré en esa estantería.",
                "Com licença, onde fica o azeite? Já procurei naquela prateleira.",
                "Scusi, dov'è l'olio d'oliva? Ho già guardato su quello scaffale.",
                "Pardon, où est l'huile d'olive ? J'ai déjà regardé sur cette étagère.",
                "죄송한데, 올리브유는 어디에 있어요? 저 선반은 이미 봤어요.",
            ),
            _t(
                "Do you have change for a twenty, or should I pay by card?",
                "¿Me puede cambiar un billete de veinte, o mejor pago con tarjeta?",
                "Tem troco para uma nota de vinte, ou é melhor eu pagar no cartão?",
                "Ha il resto per una banconota da venti, o pago con la carta?",
                "Vous avez la monnaie sur un billet de vingt, ou je paie par carte ?",
                "이십 유로짜리 잔돈 있으세요, 아니면 카드로 낼까요?",
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
                "I'd like to open a checking account for my everyday expenses.",
                "Quisiera abrir una cuenta corriente para los gastos del día a día.",
                "Eu gostaria de abrir uma conta corrente para as despesas do dia a dia.",
                "Vorrei aprire un conto corrente per le spese di tutti i giorni.",
                "Je voudrais ouvrir un compte courant pour les dépenses du quotidien.",
                "일상 생활비로 쓸 입출금 계좌를 개설하고 싶어요.",
            ),
            _t(
                "I need to withdraw some cash from the ATM just around the corner.",
                "Necesito sacar algo de dinero del cajero que está ahí a la esquina.",
                "Preciso sacar um dinheiro no caixa eletrônico bem na esquina.",
                "Devo prelevare dei contanti al bancomat proprio all'angolo.",
                "Je dois retirer un peu d'argent au distributeur, juste au coin de la rue.",
                "바로 모퉁이 ATM에서 현금을 좀 뽑아야 해요.",
            ),
            _t(
                "What's the dollar exchange rate this morning, please?",
                "¿Cuál es el tipo de cambio del dólar esta mañana, por favor?",
                "Qual é a cotação do dólar nesta manhã, por favor?",
                "Qual è il cambio del dollaro stamattina, per favore?",
                "Quel est le taux de change du dollar ce matin, s'il vous plaît ?",
                "오늘 아침 달러 환율이 어떻게 돼요?",
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
                "Which platform does the next train to Lyon leave from, please?",
                "¿De qué andén sale el próximo tren a Lyon, por favor?",
                "De qual plataforma sai o próximo trem para Lyon, por favor?",
                "Da quale binario parte il prossimo treno per Lione, per favore?",
                "C'est quel quai pour le prochain train pour Lyon, s'il vous plaît ?",
                "다음 리옹행 기차는 몇 번 승강장에서 출발해요?",
            ),
            _t(
                "Excuse me, is this seat free, or is someone sitting here?",
                "Perdón, ¿está libre este asiento, o hay alguien sentado aquí?",
                "Com licença, este assento está livre, ou tem alguém sentado aqui?",
                "Scusi, è libero questo posto, o c'è qualcuno seduto qui?",
                "Pardon, cette place est libre, ou il y a quelqu'un ici ?",
                "죄송한데, 이 자리 비어 있어요, 아니면 누가 앉은 자리예요?",
            ),
            _t(
                "We missed our connection. When is the next train toward Lyon?",
                "Perdimos el enlace. ¿Cuándo es el próximo tren hacia Lyon?",
                "Perdemos a conexão. Quando é o próximo trem para Lyon?",
                "Abbiamo perso la coincidenza. Quando c'è il prossimo treno per Lione?",
                "On a raté la correspondance. C'est quand, le prochain train pour Lyon ?",
                "환승을 놓쳤어요. 리옹 가는 다음 기차는 언제예요?",
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
                "My throat hurts and I've had a fever since this morning.",
                "Me duele la garganta y tengo fiebre desde esta mañana.",
                "Estou com dor de garganta e febre desde hoje de manhã.",
                "Ho mal di gola e la febbre da stamattina.",
                "J'ai mal à la gorge et de la fièvre depuis ce matin.",
                "목이 아프고 오늘 아침부터 열이 나요.",
            ),
            _t(
                "I twisted my ankle on the stairs and I can barely walk on it.",
                "Me torcí el tobillo en las escaleras y apenas puedo caminar.",
                "Torci o tornozelo na escada e mal consigo andar.",
                "Mi sono storciata la caviglia sulle scale e riesco a malapena a camminare.",
                "Je me suis tordu la cheville dans l'escalier et j'ai du mal à marcher.",
                "계단에서 발목을 접질러서 거의 못 걷겠어요.",
            ),
            _t(
                "Take a deep breath for me, please, then hold it there.",
                "Respire hondo, por favor, y ahora aguante el aire.",
                "Respire fundo, por favor, e agora segure o ar.",
                "Faccia un bel respiro, per favore, e ora trattenga.",
                "Respirez profondément, s'il vous plaît, et retenez comme ça.",
                "깊게 숨 들이쉬고, 그대로 참아 보세요.",
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
                "I need an appointment with the doctor as soon as you have an opening.",
                "Necesito una cita con el médico en cuanto tengan un hueco.",
                "Preciso marcar uma consulta com o médico assim que tiverem um horário.",
                "Ho bisogno di un appuntamento dal medico appena avete un buco.",
                "Il me faut un rendez-vous chez le médecin dès que vous avez une place.",
                "의사 선생님 예약, 빈 시간 생기는 대로 빨리 하고 싶어요.",
            ),
            _t(
                "Can you fill this prescription for me today, please?",
                "¿Me puede preparar esta receta hoy, por favor?",
                "Pode preparar esta receita para mim hoje, por favor?",
                "Mi può preparare questa ricetta oggi, per favore?",
                "Vous pouvez me préparer cette ordonnance aujourd'hui, s'il vous plaît ?",
                "이 처방전 오늘 조제해 주시겠어요?",
            ),
            _t(
                "I've been coughing for three days now and I can't sleep at night.",
                "Llevo ya tres días tosiendo y por la noche no puedo dormir.",
                "Já faz três dias que estou tossindo e à noite não consigo dormir.",
                "Tosso già da tre giorni e di notte non riesco proprio a dormire.",
                "Je tousse depuis trois jours maintenant et je n'arrive plus à dormir la nuit.",
                "벌써 사흘째 기침이 나서 밤에 잠을 못 자겠어요.",
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
                "I have a flat tire. Is there a gas station nearby that can help?",
                "Se me pinchó una rueda. ¿Hay una gasolinera cerca que pueda ayudarme?",
                "O pneu furou. Tem um posto por perto que possa me ajudar?",
                "Ho una gomma a terra. C'è un distributore qui vicino che possa aiutarmi?",
                "J'ai un pneu crevé. Il y a une station-service près d'ici qui pourrait m'aider ?",
                "타이어가 펑크 났어요. 도와줄 수 있는 주유소가 근처에 있어요?",
            ),
            _t(
                "Fill it up, please, with unleaded — the regular kind, not the premium.",
                "Lleno, por favor, de sin plomo, el normal, no el de 98.",
                "Completa, por favor, com gasolina comum, não a aditivada.",
                "Il pieno, per favore, di senza piombo, quella normale, non la verde.",
                "Le plein, s'il vous plaît, de sans plomb, le normal, pas le premium.",
                "무연 휘발유 보통으로 가득 넣어 주세요. 고급유는 아니고요.",
            ),
            _t(
                "I got a parking ticket even though I paid at the meter.",
                "Me pusieron una multa aunque ya había pagado el parquímetro.",
                "Levei uma multa mesmo tendo pago o parquímetro.",
                "Ho preso una multa anche se avevo già pagato il parchimetro.",
                "J'ai pris une contravention alors que j'avais déjà payé l'horodateur.",
                "주차 요금 냈는데도 벌금 딱지를 뗐어요.",
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
                "I forgot my password again and now I can't log in.",
                "Se me olvidó otra vez la contraseña y ahora no puedo entrar.",
                "Esqueci a senha de novo e agora não consigo entrar.",
                "Ho di nuovo dimenticato la password e adesso non riesco ad accedere.",
                "J'ai encore oublié mon mot de passe et je n'arrive plus à me connecter.",
                "또 비밀번호를 잊어버려서 로그인이 안 돼요.",
            ),
            _t(
                "Could you print this document for me, double-sided, please?",
                "¿Me puede imprimir este documento a doble cara, por favor?",
                "Pode imprimir este documento para mim, frente e verso, por favor?",
                "Mi può stampare questo documento fronte-retro, per favore?",
                "Vous pouvez m'imprimer ce document en recto verso, s'il vous plaît ?",
                "이 문서 양면으로 출력해 주시겠어요?",
            ),
            _t(
                "The wifi isn't working in my room at all; it was fine yesterday.",
                "El wifi no funciona en absoluto en mi habitación; ayer iba bien.",
                "O wi-fi não funciona de jeito nenhum no meu quarto; ontem estava normal.",
                "Il wifi non funziona affatto in camera mia; ieri andava bene.",
                "Le wifi ne marche plus du tout dans ma chambre ; hier ça allait encore.",
                "제 방에서 와이파이가 전혀 안 돼요. 어제는 괜찮았는데요.",
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
                "It looks really great on you. You should take it — at that price.",
                "Te queda genial de verdad. Deberías llevártelo, a ese precio.",
                "Fica ótimo em você, sério. Acho que deve levar, a esse preço.",
                "Ti sta benissimo, davvero. Dovresti prenderlo, a quel prezzo.",
                "Ça te va vraiment très bien. Tu devrais la prendre, à ce prix-là.",
                "정말 잘 어울려요. 그 가격이면 사시는 게 좋겠어요.",
            ),
            _t(
                "I'm looking for a black jacket I can wear to a wedding.",
                "Busco una chaqueta negra que pueda ponerme en una boda.",
                "Estou procurando uma jaqueta preta para usar num casamento.",
                "Cerco una giacca nera da mettere a un matrimonio.",
                "Je cherche une veste noire à porter pour un mariage.",
                "결혼식에 입을 검은 재킷을 찾고 있어요.",
            ),
            _t(
                "These shoes are too tight. Do you have them in a larger size?",
                "Estos zapatos me están estrechos. ¿Los tienen en una talla más grande?",
                "Este sapato está apertado. Vocês têm um tamanho maior?",
                "Queste scarpe sono troppo strette. Le avete in una taglia più grande?",
                "Ces chaussures sont trop étroites. Vous les avez dans une taille au-dessus ?",
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
                "It's pouring out. Did you happen to bring an umbrella with you?",
                "Está lloviendo a cántaros. ¿No habrás traído un paraguas?",
                "Está caindo um dilúvio. Você por acaso trouxe um guarda-chuva?",
                "Sta piovendo a dirotto. Hai portato l'ombrello per caso?",
                "Il pleut des cordes. T'aurais pas pris un parapluie, des fois ?",
                "밖에 비가 엄청 와요. 혹시 우산 가져왔어요?",
            ),
            _t(
                "Tomorrow will be sunny, they said, but a bit chilly in the morning.",
                "Mañana hará sol, dijeron, pero un poco de fresco por la mañana.",
                "Amanhã vai estar ensolarado, disseram, mas um pouco fresco de manhã.",
                "Domani sarà soleggiato, hanno detto, ma un po' fresco al mattino.",
                "Demain il fera soleil, à ce qu'ils disent, mais un peu frais le matin.",
                "내일은 맑다던데, 아침에는 조금 쌀쌀하대요.",
            ),
            _t(
                "What time does it usually get dark here at this time of year?",
                "¿A qué hora suele anochecer aquí a estas alturas del año?",
                "A que horas costuma escurecer aqui nesta época do ano?",
                "A che ora fa buio di solito qui in questo periodo dell'anno?",
                "Il fait nuit à quelle heure d'habitude, ici, à cette période de l'année ?",
                "이맘때 여기서는 보통 몇 시에 어두워져요?",
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
