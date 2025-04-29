import { iconProps } from '@/types/iconProps';

const IconNutrient = ({ width, height }: iconProps) => {
  return (
    <svg
      version='1.0'
      xmlns='http://www.w3.org/2000/svg'
      width={width}
      height={height}
      viewBox='0 0 64.000000 64.000000'
      preserveAspectRatio='xMidYMid meet'
    >
      <g
        transform='translate(0.000000,64.000000) scale(0.100000,-0.100000)'
        fill='#000000'
        stroke='#000000'
        strokeWidth='15'
      >
        <path
          d='M435 629 c-212 -27 -347 -98 -407 -212 -31 -60 -31 -156 0 -218 l24
-46 -20 -39 c-26 -51 -36 -100 -23 -109 6 -3 14 2 17 12 13 39 47 123 50 123
1 0 19 -10 39 -22 49 -28 165 -36 216 -14 81 34 123 100 165 256 23 90 64 170
115 228 16 18 27 37 24 43 -7 11 -103 10 -200 -2z m130 -50 c-40 -48 -71 -116
-100 -220 -53 -183 -105 -240 -221 -238 -57 0 -97 11 -138 35 -18 11 -17 15
27 77 56 78 153 168 225 209 52 30 66 48 37 48 -23 0 -120 -64 -177 -118 -28
-26 -73 -78 -101 -116 l-52 -69 -18 39 c-26 57 -18 144 20 198 78 111 253 179
476 185 l49 1 -27 -31z'
        />
      </g>
    </svg>
  );
};

export default IconNutrient;
