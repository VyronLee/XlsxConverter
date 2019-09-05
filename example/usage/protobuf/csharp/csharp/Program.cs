using System;
using System.Collections.Generic;
using System.IO;
using Google.Protobuf;
using XlsxConvert.Auto.ActorConf;
using XlsxConvert.Auto.EquipmentConf;
using XlsxConvert.Auto.Indexers;

namespace csharp
{
    internal static class Program
    {
        private const string DataDir = "../../../../../..";
        private const string ActorConf_SheetPath = DataDir + "/output/ActorConf_Properties.dat.pb";
        private const string ActorConf_IndexPath = DataDir + "/output/ActorConf_Properties.idx.pb";
        private const string EquipmentConf_SheetPath = DataDir + "/output/EquipmentConf_Properties.dat.pb";
        private const string EquipmentConf_IndexPath = DataDir + "/output/EquipmentConf_Properties.idx.pb";

        public static void Main()
        {
            Console.WriteLine("Dump ActorConf.Properties:");
            var actorSheet = LoadAndParseFromFile<ActorConf_Properties_Sheet>(ActorConf_SheetPath);
            foreach (var record in actorSheet.Data)
                Console.WriteLine(record);

            var indexes = LoadAndParseFromFile<XlsxRecordIndexes>(ActorConf_IndexPath);
            for (var i = 0; i < 4; i++)
            {
                var idx = GetRecordIndex(indexes, "id", i + 1);
                Console.WriteLine("Query record with 'id': " + (i + 1));
                if (idx >= 0)
                    Console.WriteLine(actorSheet.Data[idx]);
                else
                    Console.WriteLine("Not found!");
            }

            Console.WriteLine("Dump EquipmentConf.Properties:");
            var equipmentSheet = LoadAndParseFromFile<EquipmentConf_Properties_Sheet>(EquipmentConf_SheetPath);
            foreach (var record in equipmentSheet.Data)
                Console.WriteLine(record);

            indexes = LoadAndParseFromFile<XlsxRecordIndexes>(EquipmentConf_IndexPath);
            for (var i = 0; i < 4; i++)
            {
                var idx = GetRecordIndex(indexes, "id", i + 1, "quality", 1);
                Console.WriteLine("Query record with 'id': {0} and 'quality': 1", i + 1);
                if (idx >= 0)
                    Console.WriteLine(equipmentSheet.Data[idx]);
                else
                    Console.WriteLine("Not found!");
            }
        }

        private static T LoadAndParseFromFile<T>(string path) where T: IMessage<T>, new()
        {
            var bytes = File.ReadAllBytes(path);
            var obj = new MessageParser<T>(() => new T()).ParseFrom(bytes);
            return obj;
        }

        private static int GetRecordIndex<T>(XlsxRecordIndexes indexes, string key, T value)
        {
            var ids = GetRecordIndexes(indexes, key, value);
            if (ids == null)
                return -1;

            return ids.Count > 0 ? ids[0] : -1;
        }

        private static IList<int> GetRecordIndexes<T>(XlsxRecordIndexes indexes, string key, T value)
        {
            if (!indexes.Values.TryGetValue(key, out var values))
                 throw new KeyNotFoundException("No key defined in sheet: " + key);

            if (values.Values.TryGetValue(value.ToString(), out var ids))
                return ids.Values;

            return null;
        }

        private static int GetRecordIndex<T1, T2>(XlsxRecordIndexes indexes, string key1, T1 value1, string key2, T2 value2)
        {
            var ids = GetRecordIndexes(indexes, key1, value1, key2, value2);
            if (ids == null)
                return -1;

            return ids.Count > 0 ? ids[0] : -1;
        }

        private static IList<int> GetRecordIndexes<T1, T2>(XlsxRecordIndexes indexes, string key1, T1 value1, string key2, T2 value2)
        {
            var keyHash = $"{key1}-{key2}";
            if (!indexes.Values.TryGetValue( keyHash, out var values))
                 throw new KeyNotFoundException("No key defined in sheet: " +  keyHash);

            var valueHash = $"{value1.ToString()}-{value2.ToString()}";
            if (values.Values.TryGetValue(valueHash, out var ids))
                return ids.Values;

            return null;
        }

    }
}