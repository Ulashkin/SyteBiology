using System.Diagnostics;
using static System.Console;
using System.Collections;
using ConsoleApp52;
using System.Runtime.CompilerServices;
using System.Collections.Generic;

namespace ConsoleApp52
{

    interface IWord
    {
        string GetWord();    
        int GetWordCount { get; }                             
    }


    public
   class WordFrequence : IWord
    {
        string word;

        int count;
        private string key;

        public string Word { get; set; }
            public int Count { get; set; }

        public WordFrequence(string word, int count)
        {
            this.word = word;
            this.count = 0;
        }

        public WordFrequence(string key)
        {
            this.key = key;
        }

        int IWord.GetWordCount => throw new NotImplementedException();

        public string GetWord()
        {
            return word;
        }



        public override string ToString()
        {
            return $"{word}:{count}";
        }

        public static WordFrequence operator ++(WordFrequence wordFrequence)
        {
            wordFrequence.count++;
            return wordFrequence;
        }
    }

    public class DictionaryFrequence
    {
        private Dictionary<string, int> AW;

        public DictionaryFrequence()
        {
            AW = new Dictionary<string, int>();
        }

        public void ReadFromFile(string ulas)
        {
            string[] words = File.ReadAllText(ulas).Split(GetDelimiterChars(), StringSplitOptions.RemoveEmptyEntries);

            foreach (string word in words)
            {
                if (AW.ContainsKey(word))
                {
                    AW[word]++;
                }
                else
                {
                    AW[word] = 1;
                }
            }
    }

        public void SaveResultsToFile(string ulas)
        {
            using (StreamWriter writer = new StreamWriter(ulas))
            {
                writer.WriteLine($"hello my Friend: {AW.Values.Sum()}");

                foreach (KeyValuePair<string, int> pair in AW)
                {
                    writer.WriteLine($"{pair.Key} : {pair.Value}");
                }
            }
        }

        public int this[string word]
        {
            get
            {
                if (AW.ContainsKey(word))
                {
                    return AW[word];
                }
                else
                {
                    return 0;
                }
            }
        }

        public void Print()
        {
            AW.ToList().ForEach(pair => WriteLine($"{pair.Key} : {pair.Value}"));
        }

        public WordFrequence[] ToWordFrequence()
        {
            return AW.Select(pair => new WordFrequence(pair.Key) { Count = pair.Value }).ToArray();
        }

        public override string ToString()
        {
            return string.Join(Environment.NewLine, AW.Select(pair => $"{pair.Key} : {pair.Value}"));
        }

        private char[] GetDelimiterChars()
        {
            return new char[] { ' ', '.', ';',' ' };
    }
    }

       


        public class ProcessDictionary
    {
        public  void SortAlphabet (WordFrequence[] WF)
        {
        Array.Sort(WF);
        }


        public WordFrequence[] SortFrequence(DictionaryFrequence df)
        {
            return SortFrequence(df);
        }


        public WordFrequence[] SortAlphabetLINQ(WordFrequence[] WF)

        {
            IEnumerable<IGrouping<string, string>> query =
    (IEnumerable<IGrouping<string, string>>)(from i in WF
    orderby i descending
    select i); return SortAlphabetLINQ (WF);
    


    
        }





    }



}




internal class Program
    {
        static void Main(string[] args)
        {
        DictionaryFrequence df = new DictionaryFrequence();

     df.Print();
    
        ProcessDictionary   pd=new ProcessDictionary();



        df.ReadFromFile("input.txt");
        df.SaveResultsToFile("output.txt");
       //WriteLine(df["hello"]);
       df.Print();
       
    }
    }
