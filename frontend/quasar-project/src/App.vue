<template>
  <router-view />
</template>

<script setup>
import { provide, ref } from 'vue';


const response = ref ([
  { id: 40, userId: 1, latitude: 52.358, longitude: 4.868, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.868,52.358]}' },
  { id: 2, userId: 2, latitude: 52.355, longitude: 4.956, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.956,52.355]}' },
  { id: 15, userId: 2, latitude: 52.369, longitude: 4.846, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.846,52.369]}' },
  { id: 31, userId: 1, latitude: 52.364, longitude: 4.934, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.934,52.364]}' },
  { id: 5, userId: 5, latitude: 52.358, longitude: 4.962, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.962,52.358]}' },
  { id: 22, userId: 4, latitude: 52.358793, longitude: 4.867782, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.867782,52.358793]}' },
  { id: 50, userId: 1, latitude: 52.354709, longitude: 4.855900, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.855900,52.354709]}' },
  { id: 10, userId: 5, latitude: 52.357, longitude: 4.958, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
  { id: 33, userId: 3, latitude: 52.374, longitude: 4.891, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.891,52.374]}' },
  { id: 27, userId: 4, latitude: 52.371, longitude: 4.844, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.844,52.371]}' },
  { id: 45, userId: 1, latitude: 52.359473, longitude: 4.875700, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.875700,52.359473]}' },
  { id: 18, userId: 5, latitude: 52.366, longitude: 4.936, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.936,52.366]}' },
  { id: 7, userId: 2, latitude: 52.354, longitude: 4.952, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.952,52.354]}' },
  { id: 55, userId: 1, latitude: 52.342, longitude: 4.892, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.892,52.342]}' },
  { id: 36, userId: 1, latitude: 52.355379, longitude: 4.856230, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.856230,52.355379]}' },
  { id: 60, userId: 1, latitude: 52.372, longitude: 4.893, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.893,52.372]}' },
  { id: 14, userId: 1, latitude: 52.376, longitude: 4.889, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.889,52.376]}' },
  { id: 49, userId: 5, latitude: 52.355919, longitude: 4.858136, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.858136,52.355919]}' },
  { id: 3, userId: 3, latitude: 52.356, longitude: 4.958, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.958,52.356]}' },
  { id: 58, userId: 4, latitude: 52.365, longitude: 4.850, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.850,52.365]}' },
  { id: 25, userId: 2, latitude: 52.365, longitude: 4.978, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.978,52.365]}' },
  { id: 42, userId: 3, latitude: 52.359758, longitude: 4.873774, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.873774,52.359758]}' },
  { id: 6, userId: 1, latitude: 52.353, longitude: 4.950, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.950,52.353]}' },
  { id: 51, userId: 2, latitude: 52.390, longitude: 4.910, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.910,52.390]}' },
  { id: 29, userId: 1, latitude: 52.368, longitude: 4.938, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.938,52.368]}' },
  { id: 37, userId: 2, latitude: 52.356381, longitude: 4.861177, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.861177,52.356381]}' },
  { id: 64, userId: 5, latitude: 52.357, longitude: 4.958, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
  { id: 12, userId: 2, latitude: 52.362, longitude: 4.972, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.972,52.362]}' },
  { id: 21, userId: 3, latitude: 52.356913, longitude: 4.865376, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.865376,52.356913]}' },
  { id: 48, userId: 4, latitude: 52.355172, longitude: 4.866809, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.866809,52.355172]}' },
  { id: 17, userId: 4, latitude: 52.346, longitude: 4.896, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.896,52.346]}' },
  { id: 54, userId: 5, latitude: 52.362, longitude: 4.932, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.932,52.362]}' },
  { id: 35, userId: 5, latitude: 52.392, longitude: 4.912, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.912,52.392]}' },
  { id: 1, userId: 1, latitude: 52.354, longitude: 4.954, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.954,52.354]}' },
  { id: 43, userId: 4, latitude: 52.359470, longitude: 4.875362, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.875362,52.359470]}' },
  { id: 24, userId: 1, latitude: 52.364, longitude: 4.976, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.976,52.364]}' },
  { id: 59, userId: 5, latitude: 52.370, longitude: 4.895, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.895,52.370]}' },
  { id: 8, userId: 3, latitude: 52.355, longitude: 4.954, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.954,52.355]}' },
  { id: 46, userId: 2, latitude: 52.360603, longitude: 4.876070, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.876070,52.360603]}' },
  { id: 32, userId: 2, latitude: 52.340, longitude: 4.890, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.890,52.340]}' },
  { id: 53, userId: 4, latitude: 52.360, longitude: 4.930, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.930,52.360]}' },
  { id: 19, userId: 1, latitude: 52.394, longitude: 4.914, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.914,52.394]}' },
  { id: 56, userId: 2, latitude: 52.344, longitude: 4.894, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.894,52.344]}' },
  { id: 38, userId: 3, latitude: 52.357528, longitude: 4.863913, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.863913,52.357528]}' },
  { id: 4, userId: 4, latitude: 52.357, longitude: 4.960, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.960,52.357]}' },
  { id: 61, userId: 2, latitude: 52.357, longitude: 4.958, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
  { id: 13, userId: 3, latitude: 52.363, longitude: 4.974, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.974,52.363]}' },
  { id: 52, userId: 3, latitude: 52.398, longitude: 4.918, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.918,52.398]}' },
  { id: 23, userId: 5, latitude: 52.357832, longitude: 4.869069, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.869069,52.357832]}' },
  { id: 34, userId: 4, latitude: 52.367, longitude: 4.848, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.848,52.367]}' },
  { id: 41, userId: 2, latitude: 52.358638, longitude: 4.870776, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.870776,52.358638]}' },
  { id: 16, userId: 3, latitude: 52.369, longitude: 4.846, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.846,52.369]}' },
  { id: 57, userId: 3, latitude: 52.373, longitude: 4.842, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.842,52.373]}' },
  { id: 39, userId: 4, latitude: 52.357528, longitude: 4.863913, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.863913,52.357528]}' },
  { id: 62, userId: 3, latitude: 52.357, longitude: 4.958, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
  { id: 9, userId: 4, latitude: 52.356, longitude: 4.956, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.956,52.356]}' },
  { id: 63, userId: 4, latitude: 52.357, longitude: 4.958, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
  { id: 20, userId: 2, latitude: 52.356913, longitude: 4.865376, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.865376,52.356913]}' },
  { id: 65, userId: 1, latitude: 52.361230, longitude: 4.880370, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.880370,52.361230]}' },
  { id: 44, userId: 5, latitude: 52.360223, longitude: 4.871586, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.871586,52.360223]}' },
  { id: 26, userId: 3, latitude: 52.378, longitude: 4.887, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.887,52.378]}' },
  { id: 47, userId: 3, latitude: 52.358533, longitude: 4.874794, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.874794,52.358533]}' },
  { id: 28, userId: 5, latitude: 52.348, longitude: 4.898, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.898,52.348]}' },
  { id: 30, userId: 2, latitude: 52.396, longitude: 4.916, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.916,52.396]}' },
  { id: 11, userId: 1, latitude: 52.361, longitude: 4.970, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.970,52.361]}' },
  {
      "id": 66,
      "userId": "1",
      "latitude": 47.2298577,
      "longitude": 16.6210284,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210284,47.2298577]}"
  },
  {
      "id": 67,
      "userId": "1",
      "latitude": 47.2298577,
      "longitude": 16.6210284,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210284,47.2298577]}"
  },
  {
      "id": 68,
      "userId": "1",
      "latitude": 47.2298577,
      "longitude": 16.6210284,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210284,47.2298577]}"
  },
  {
      "id": 69,
      "userId": "1",
      "latitude": 47.2298577,
      "longitude": 16.6210284,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210284,47.2298577]}"
  },
  {
      "id": 70,
      "userId": "1",
      "latitude": 47.2298814,
      "longitude": 16.621045,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621045,47.2298814]}"
  },
  {
      "id": 71,
      "userId": "1",
      "latitude": 47.2298814,
      "longitude": 16.621045,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621045,47.2298814]}"
  },
  {
      "id": 72,
      "userId": "1",
      "latitude": 47.247575604026075,
      "longitude": 16.589023297799972,
      "stress_level": 3,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.589023297799972,47.247575604026075]}"
  },
  {
      "id": 73,
      "userId": "1",
      "latitude": 47.2298687,
      "longitude": 16.6210426,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210426,47.2298687]}"
  },
  {
      "id": 74,
      "userId": "1",
      "latitude": 47.2298687,
      "longitude": 16.6210426,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210426,47.2298687]}"
  },
  {
      "id": 75,
      "userId": "1",
      "latitude": 47.2298687,
      "longitude": 16.6210426,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210426,47.2298687]}"
  },
  {
      "id": 76,
      "userId": "1",
      "latitude": 47.2298882,
      "longitude": 16.6210537,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210537,47.2298882]}"
  },
  {
      "id": 77,
      "userId": "1",
      "latitude": 47.2298882,
      "longitude": 16.6210537,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210537,47.2298882]}"
  },
  {
      "id": 78,
      "userId": "1",
      "latitude": 47.2298882,
      "longitude": 16.6210537,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210537,47.2298882]}"
  },
  {
      "id": 79,
      "userId": "1",
      "latitude": 47.2298882,
      "longitude": 16.6210537,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210537,47.2298882]}"
  },
  {
      "id": 80,
      "userId": "1",
      "latitude": 47.2298882,
      "longitude": 16.6210537,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210537,47.2298882]}"
  },
  {
      "id": 81,
      "userId": "1",
      "latitude": 47.2298882,
      "longitude": 16.6210537,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210537,47.2298882]}"
  },
  {
      "id": 82,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 83,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 84,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 85,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 86,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 87,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 88,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 89,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 90,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 91,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 92,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 93,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 94,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 95,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 96,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 97,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 98,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 99,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 100,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 101,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 102,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 103,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 104,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 105,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 106,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 107,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 108,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 109,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 110,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 111,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 112,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 113,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 114,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 115,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 116,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 117,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 118,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 119,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 120,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 121,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 122,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 123,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 124,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 125,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 126,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 127,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 128,
      "userId": "1",
      "latitude": 47.2298755,
      "longitude": 16.6210405,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210405,47.2298755]}"
  },
  {
      "id": 129,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 2,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 130,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 131,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 132,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 133,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 134,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 135,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 136,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 137,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 138,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 139,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 140,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 141,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 142,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 143,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 144,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 145,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 146,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 147,
      "userId": "1",
      "latitude": 47.22985433227367,
      "longitude": 16.621021713621996,
      "stress_level": 1,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.621021713621996,47.22985433227367]}"
  },
  {
      "id": 148,
      "userId": "1",
      "latitude": 53.00250305630031,
      "longitude": 17.95320159423565,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[17.95320159423565,53.00250305630031]}"
  },
  {
      "id": 149,
      "userId": "1",
      "latitude": 53.00250305630031,
      "longitude": 17.95320159423565,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[17.95320159423565,53.00250305630031]}"
  },
  {
      "id": 150,
      "userId": "1",
      "latitude": 53.00250305630031,
      "longitude": 17.95320159423565,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[17.95320159423565,53.00250305630031]}"
  },
  {
      "id": 151,
      "userId": "1",
      "latitude": 53.00250305630031,
      "longitude": 17.95320159423565,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[17.95320159423565,53.00250305630031]}"
  },
  {
      "id": 152,
      "userId": "1",
      "latitude": 53.00250305630031,
      "longitude": 17.95320159423565,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[17.95320159423565,53.00250305630031]}"
  },
  {
      "id": 153,
      "userId": 1,
      "latitude": 52.377956,
      "longitude": 4.89707,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[4.89707,52.377956]}"
  },
  {
      "id": 154,
      "userId": 1,
      "latitude": 47.2298586,
      "longitude": 16.6210268,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210268,47.2298586]}"
  },
  {
      "id": 155,
      "userId": 1,
      "latitude": 47.2298586,
      "longitude": 16.6210268,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210268,47.2298586]}"
  },
  {
      "id": 156,
      "userId": 1,
      "latitude": 47.2298586,
      "longitude": 16.6210268,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210268,47.2298586]}"
  },
  {
      "id": 157,
      "userId": 1,
      "latitude": 47.2298864,
      "longitude": 16.6210559,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210559,47.2298864]}"
  },
  {
      "id": 158,
      "userId": 1,
      "latitude": 47.2298864,
      "longitude": 16.6210559,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210559,47.2298864]}"
  },
  {
      "id": 159,
      "userId": 1,
      "latitude": 47.2298864,
      "longitude": 16.6210559,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210559,47.2298864]}"
  },
  {
      "id": 160,
      "userId": 1,
      "latitude": 47.2298864,
      "longitude": 16.6210559,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210559,47.2298864]}"
  },
  {
      "id": 161,
      "userId": 1,
      "latitude": 47.2298864,
      "longitude": 16.6210559,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210559,47.2298864]}"
  },
  {
      "id": 162,
      "userId": 1,
      "latitude": 47.2298864,
      "longitude": 16.6210559,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210559,47.2298864]}"
  },
  {
      "id": 163,
      "userId": 1,
      "latitude": 47.2298864,
      "longitude": 16.6210559,
      "stress_level": 4,
      "geom": "{\"type\":\"Point\",\"coordinates\":[16.6210559,47.2298864]}"
  }
]);

provide('response', response);

if (!localStorage.getItem('response') || localStorage.getItem('response') === "[]") {
  localStorage.setItem('response', JSON.stringify(response));
}

</script>
