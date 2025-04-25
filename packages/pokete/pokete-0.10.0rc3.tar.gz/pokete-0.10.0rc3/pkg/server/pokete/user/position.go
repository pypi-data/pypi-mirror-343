package user

import (
	"errors"
	"fmt"
	"slices"
)

var POSITION_ERROR = errors.New("unplaussible position")

type Position struct {
	Map string `json:"map"`
	X   uint64 `json:"x"`
	Y   uint32 `json:"y"`
}

func (p *Position) Change(newPosition Position) error {
	if p.isPlausible(newPosition) {
		p.Map = newPosition.Map
		p.X = newPosition.X
		p.Y = newPosition.Y
		return nil
	}
	return errors.Join(POSITION_ERROR, fmt.Errorf("position %v is not plausible to result from %v", newPosition, *p))
}

func (p Position) isPlausible(newPosition Position) bool {
	return p.Map != newPosition.Map || slices.Contains(
		[]Position{
			{p.Map, p.X, p.Y + 1},
			{p.Map, p.X, p.Y - 1},
			{p.Map, p.X + 1, p.Y},
			{p.Map, p.X - 1, p.Y},
			p,
		},
		newPosition,
	)
}
