import Nim
import Data.Char (ord)


readNim :: IO Nim
readNim = fromInteger <$> read <$> getLine

encode :: [Char] -> [Nim]
encode x = map (fromIntegral . ord) x

isValidKey :: Nim -> Int -> Bool
isValidKey key n = isUnityRoot && isPrimitive
    where
        isUnityRoot = key ^ n == 1
        isPrimitive = not $ elem 1 [ key ^ i | i <- [1..n-1] ]

encrypt :: Nim -> [Nim] -> [Nim]
encrypt key message
    | isValidKey key n = zipWith (+) keys [ calc x | x <- keys ]   # calc 랑 key 랑 각 배열 합
    | otherwise        = error "Invalid key"
    where
        n    = length message
        keys = pows key
        coef = reverse $ zipWith (*) message keys   # message 와 keys각 항 곱해서 reverse
        pows = \val -> [ val ^ i | i <- [0..n-1] ]  # pow들의 집합 (0~n-1)
        calc = \val -> sum $ zipWith (*) coef (pows val)

main :: IO ()
main = do
    putStrLn "Enter flag to encrypt:"
    flag <- getLine
    putStrLn "Enter your key:"
    key <- readNim
    putStrLn "Your encrypted flag:"
    print $ encrypt key (encode flag)
