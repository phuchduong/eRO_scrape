# Encodings
# Codec         | Aliases                                               | Languages
# cp850         | 850, IBM850                                           | Western Europe
# cp1252        | windows-1252                                          | Western Europe
# latin_1       | iso-8859-1, iso8859-1, 8859, cp819, latin, latin1, L1 | West Europe
# iso8859_3     | iso-8859-3, latin3, L3                                | Esperanto, Maltese
# iso8859_15    | iso-8859-15                                           | Western Europe
codecs = [
    "cp850",
    "cp1252",
    "latin_1",
    "iso8859_3",
    "iso8859_15",
    "cp437",
    "cp1256",
    "cp1257",
    "iso8859_2",
    "iso8859_4",
    "iso8859_5",
    "iso8859_6",
    "iso8859_7",
    "iso8859_8",
    "iso8859_9",
    "iso8859_10",
    "iso8859_13",
    "iso8859_14",
    "cp1250",
    "cp1251",
    "cp866",
    "koi8_r",
    "koi8_u",
    "cp1253",
    "cp1255",
    "cp1254",
    "cp1258",
]
works = []
for codec in codecs:
    try:
        main(codec=codec)
        works.append(codec)
    except (UnicodeDecodeError, UnicodeEncodeError) as e:
        print("--------------------------------")
        print("Error in codec: " + codec + ". Error: " + str(e))
        print("--------------------------------")
        pass
print("--------------------------------")
print("Script Finished-----------------")
print("These codecs work:")
print(",".join(works))
