from lesk import (
    classical_lesk,
    show_all_senses, get_sense_label, get_sense_text,
)
from semantic_relations import get_all_relations

def print_relations(sense):
    rels = get_all_relations(sense)
    print("   Синонимы:  ", rels['synonyms'] if rels['synonyms'] else "(нет)")
    print("   Гиперонимы:", rels['hypernyms'] if rels['hypernyms'] else "(нет)")
    print("   Гипонимы:  ", rels['hyponyms'] if rels['hyponyms'] else "(нет)")

def print_result(label, result):
    if result is None:
        print(f"{label}: слово не нашлось в тезаурусе.")
        return
    best_sense, score = result
    print(f"\n{label}:")
    print(f"   Синсет:     [{get_sense_label(best_sense)}]")
    definition = get_sense_text(best_sense)
    if len(definition) > 200:
        definition = definition[:200] + "..."
    print(f"   Определение: {definition}")
    print(f"   Score (совпадений): {score}")
    print("   Семантические отношения:")
    print_relations(best_sense)

def run_example(sentence, target_word):
    print("=" * 75)
    print("Предложение:", sentence)
    print("Отмеченное слово:", target_word)
    print("=" * 75)
    
    print("\n--- Все значения слова: ---")
    show_all_senses(target_word)
    
    print("\n--- Результаты WSD: ---")
    
    result_classic = classical_lesk(target_word, sentence)
    print_result("[КЛАССИЧЕСКИЙ Леск]", result_classic)

def run_demo():
    run_example(
        sentence="Я буду сдавать лабораторные работы вовремя и получу хорошую оценку за экзамен.",
        target_word="оценка"
    )
    
    run_example(
        sentence="Он высказал своё мнение и дал критическую оценку работе коллеги.",
        target_word="оценка"
    )
    
    run_example(
        sentence="Чтобы открыть дверь квартиры, мне нужен ключ от замка.",
        target_word="ключ"
    )
    
    run_example(
        sentence="Для салата я купил зелёный лук и свежие помидоры.",
        target_word="лук"
    )

    run_example(
        sentence="В среду у нас назначено совещание по новому проекту.",
        target_word="среда"
    )

    run_example(
        sentence="Он взял ручку и аккуратно подписал все страницы договора.",
        target_word="ручка"
    )

    run_example(
        sentence="Осенью зелёный вегетативный лист клёна желтеет и опадает с ветки растения.",
        target_word="лист"
    )

    run_example(
        sentence="Переговоры завершились успехом и стороны подписали договор о мире, прекратив войну.",
        target_word="мир"
    )

    run_example(
        sentence="Стоматолог попросил открыть рот и высунуть язык для осмотра полости.",
        target_word="язык"
    )

    run_example(
        sentence="Фермер вспахал верхний слой почвы и посадил пшеницу на широком поле.",
        target_word="земля"
    )


def run_interactive():
    print("\n=== Интерактивный режим ===")
    print("(чтобы выйти — введите пустое предложение)\n")
    
    while True:
        sentence = input("Введите предложение: ").strip()
        if sentence == "":
            print("Выход.")
            break
        target_word = input("Введите отмеченное слово: ").strip()
        if target_word == "":
            print("Слово не введено, пропускаю.")
            continue
        
        if target_word.lower() not in sentence.lower():
            print(f"ВНИМАНИЕ: слово '{target_word}' не встречается в предложении. "
                  f"Алгоритм всё равно попробует сработать.")
        
        run_example(sentence, target_word)

def main():
    print("Что запустить?")
    print("  1 — демо (готовые примеры)")
    print("  2 — интерактивный режим (ввести свой пример)")
    choice = input("Ваш выбор [1/2]: ").strip()
    
    if choice == "1":
        run_demo()
    elif choice == "2":
        run_interactive()
    else:
        print("Непонятно, запускаю демо...")
        run_demo()

if __name__ == "__main__":
    main()