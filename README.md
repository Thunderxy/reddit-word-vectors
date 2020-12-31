# RWV (Reddit Word Vectors)
- downloads reddit posts and comments from pushshift using threads
- makes Word2vec, Doc2vec or FastText model from extracted sentences using Gensim library

See example.ipynb for more info on how to use this script.  
Example word2vec model can be found [here](https://github.com/NightThunder/RAT/releases).

## Results
50 most similar words to "cat" (float is cosine similarity):  
dog: 0.84 puppy: 0.71 kitten: 0.69 pup: 0.69 chihuahua: 0.68 husky: 0.65 pug: 0.65 cats: 0.62 kitty: 0.61 bird: 0.61 beagle: 0.60 cockatiel: 0.59 rottweiler: 0.59 neighbor: 0.59 dachshund: 0.58 toddler: 0.58 pet: 0.57 daughter: 0.57 pitbull: 0.57 corgi: 0.55 grandma: 0.55 baby: 0.55 pupper: 0.55 son: 0.54 girlfriend: 0.54 husband: 0.54 boyfriend: 0.54 tabby: 0.54 gerbil: 0.54 hamster: 0.54 doggo: 0.53 dogs: 0.53 chinchilla: 0.53 parakeet: 0.53 mutt: 0.53 mom: 0.53 roommate: 0.53 sister: 0.52 poodle: 0.52 ferret: 0.52 wife: 0.52 parrot: 0.52 dad: 0.51 gf: 0.51 brother: 0.51 yorkie: 0.51 cousin: 0.51 squirrel: 0.51 neighbour: 0.51 goldfish: 0.51  

50 most similar words to "python":  
matlab: 0.82 java: 0.75 javascript: 0.74 fortran: 0.74 mathematica: 0.70 perl: 0.69 haskell: 0.67 matplotlib: 0.67 sympy: 0.66 scipy: 0.65 numpy: 0.65 labview: 0.64 sql: 0.63 php: 0.63 vim: 0.62 vba: 0.62 cython: 0.62 cuda: 0.62 tikz: 0.61 programming: 0.61 idl: 0.61 gnuplot: 0.60 scilab: 0.60 latex: 0.60 ocaml: 0.59 numpyscipy: 0.59 matlaboctave: 0.57 spss: 0.57 clojure: 0.57 coding: 0.56 scala: 0.56 openmp: 0.56 html: 0.56 auctex: 0.55 scripting: 0.55 lua: 0.54 cobol: 0.54 tensorflow: 0.54 gmp: 0.54 pythons: 0.53 linux: 0.53 lyx: 0.53 tex: 0.53 uestevilka: 0.52 solidworks: 0.52 jupyter: 0.52 sage: 0.52 compiler: 0.52 texmaker: 0.51 mathlab: 0.51  
